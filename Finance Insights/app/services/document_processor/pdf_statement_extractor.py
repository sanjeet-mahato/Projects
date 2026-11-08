import logging
from collections import defaultdict
from pathlib import Path

import camelot

from app.services.apploadconfig import config
from app.services.document_processor.physical_table import PhysicalTable
from app.services.document_processor.logical_table import LogicalTable


logger = logging.getLogger(__name__)


class PDFStatementExtractor:
    """Extract physical PDF tables and combine them into logical tables."""

    def __init__(self, pdf_path: str | Path, pages: str = "all"):
        self.pdf_path = Path(pdf_path)
        self.pages = pages

        # Load logical table matching configuration.
        logical_config = config["logical_table"]

        self.similarity_threshold = float(
            logical_config["similarity_threshold"]
        )

        # Exact header matches contribute positive bonuses to similarity.
        self.bonuses = {
            "headers": float(logical_config["header_bonus"]),
            "headers_extras": float(
                logical_config["headers_extras_bonus"]
            ),
        }

        # Validate that individual bonuses are non-negative.
        if any(bonus < 0 for bonus in self.bonuses.values()):
            raise ValueError("Similarity bonuses cannot be negative.")

        # Combined bonuses must not increase similarity beyond 1.
        if sum(self.bonuses.values()) > 1:
            raise ValueError("Combined similarity bonuses cannot exceed 1.")

        # Validate the minimum similarity required to match tables.
        if not 0 <= self.similarity_threshold <= 1:
            raise ValueError("Similarity threshold must be between 0 and 1.")

        self.logical_tables: list[LogicalTable] = []

    def extract(self) -> list[LogicalTable]:
        """Extract and combine tables from the PDF."""

        logger.info(
            "Starting PDF table extraction | PDF: %s | Pages: %s",
            self.pdf_path,
            self.pages,
        )

        # Extract physical tables from the PDF using Camelot.
        camelot_tables = camelot.read_pdf(
            str(self.pdf_path),
            pages=self.pages,
            flavor="lattice",
            parallel=True,
            cpu_count=4,
        )

        logger.info(
            "Camelot extraction completed\n"
            "  PDF             : %s\n"
            "  Physical tables : %s",
            self.pdf_path,
            len(camelot_tables),
        )

        # Group extracted physical tables by their PDF page number.
        page_tables = defaultdict(list)

        for camelot_table in camelot_tables:
            physical_table = PhysicalTable(camelot_table)

            # Ignore tables without any extracted rows.
            if physical_table.row_count == 0:
                logger.debug(
                    "Skipping empty physical table | Page: %s",
                    physical_table.page,
                )
                continue

            page_tables[physical_table.page].append(physical_table)

        # Report how many physical tables were found on each page.
        for page_number in sorted(page_tables):
            logger.info(
                "Page %s | Found %s physical table(s)",
                page_number,
                len(page_tables[page_number]),
            )

        # Reset previous extraction results before processing the PDF.
        self.logical_tables = []
        previous_page_tables = []

        # Process pages in ascending order.
        for page_number in sorted(page_tables):
            # Create a logical table candidate for every physical table.
            candidates = [
                LogicalTable(physical_table)
                for physical_table in page_tables[page_number]
            ]

            # The first page has no previous tables to compare against.
            if not previous_page_tables:
                self.logical_tables.extend(candidates)
                previous_page_tables = candidates

                # logging details for new logical tables
                for candidate in candidates:
                    logger.info(
                        "New logical table created\n"
                        "  Pages   : %s-%s\n"
                        "  Columns : %s\n"
                        "  Rows    : %s",
                        candidate.pages[0],
                        candidate.pages[-1],
                        candidate.column_count,
                        candidate.row_count,
                    )

                continue

            # Find one-to-one matches with tables from the previous page.
            matches = self._match_tables(
                previous_page_tables,
                candidates,
            )

            current_page_tables = []
            matched_candidates = set()

            # Merge matched candidates into their corresponding logical tables.
            for previous_index, candidate_index in matches:
                target = previous_page_tables[previous_index]
                candidate = candidates[candidate_index]

                # Reuse the target headers when the candidate headers differ.
                if candidate.headers != target.headers:
                    candidate.update_headers(
                        headers=target.headers,
                        headers_extras=target.headers_extras,
                        move_current_to_data=bool(candidate.headers),
                    )

                target.append_table(candidate)

                logger.info(
                    "Physical table merged into logical table\n"
                    "  Current page  : %s\n"
                    "  Logical table : Pages %s-%s\n"
                    "  Rows added    : %s\n"
                    "  Total rows    : %s",
                    page_number,
                    target.pages[0],
                    target.pages[-1],
                    candidate.row_count,
                    target.row_count,
                )

                current_page_tables.append(target)
                matched_candidates.add(candidate_index)

            # Unmatched candidates represent new logical tables.
            new_logical_tables = [
                candidate
                for index, candidate in enumerate(candidates)
                if index not in matched_candidates
            ]

            self.logical_tables.extend(new_logical_tables)
            current_page_tables.extend(new_logical_tables)

            for candidate in new_logical_tables:
                logger.info(
                    "New logical table created\n"
                    "  Pages   : %s-%s\n"
                    "  Columns : %s\n"
                    "  Rows    : %s",
                    candidate.pages[0],
                    candidate.pages[-1],
                    candidate.column_count,
                    candidate.row_count,
                )

            # Only tables present on the current page are considered
            # for matching against the next page.
            previous_page_tables = current_page_tables

        logger.info(
            "PDF table extraction completed\n"
            "  PDF             : %s\n"
            "  Physical tables : %s\n"
            "  Logical tables  : %s",
            self.pdf_path,
            sum(len(tables) for tables in page_tables.values()),
            len(self.logical_tables),
        )

        return self.logical_tables

    def _match_tables(
        self,
        previous_tables: list[LogicalTable],
        current_tables: list[LogicalTable],
    ) -> list[tuple[int, int]]:
        """Find one-to-one matches between consecutive pages."""

        possible_matches = []

        # Calculate similarity between every possible table pair.
        for previous_index, existing_table in enumerate(previous_tables):
            for candidate_index, candidate_table in enumerate(current_tables):
                similarity = self._get_similarity(
                    existing_table,
                    candidate_table,
                )

                # Retain only pairs meeting the configured threshold.
                if similarity >= self.similarity_threshold:
                    possible_matches.append(
                        (similarity, previous_index, candidate_index)
                    )

        # Consider the highest-scoring pairs first.
        possible_matches.sort(
            key=lambda match: match[0],
            reverse=True,
        )

        matched_previous = set()
        matched_current = set()
        matches = []

        # Assign each previous and current table to at most one match.
        for similarity, previous_index, candidate_index in possible_matches:
            if previous_index in matched_previous:
                continue

            if candidate_index in matched_current:
                continue

            matches.append((previous_index, candidate_index))

            matched_previous.add(previous_index)
            matched_current.add(candidate_index)

            logger.debug(
                "Accepted table match\n"
                "  Existing logical table : Pages %s-%s\n"
                "  Current-page candidate : Page %s\n"
                "  Similarity             : %.4f",
                previous_tables[previous_index].pages[0],
                previous_tables[previous_index].pages[-1],
                current_tables[candidate_index].pages[0],
                similarity,
            )

        return matches

    def _get_similarity(
        self,
        existing_table: LogicalTable,
        candidate_table: LogicalTable,
    ) -> float:
        """Calculate continuation similarity with exact-match bonuses."""

        # Tables with different column counts cannot match.
        if existing_table.column_count != candidate_table.column_count:
            logger.debug(
                "Continuation comparison skipped\n"
                "  Existing logical table : Pages %s-%s\n"
                "  Current-page candidate : Page %s\n"
                "  Existing columns       : %s\n"
                "  Candidate columns      : %s",
                existing_table.pages[0],
                existing_table.pages[-1],
                candidate_table.pages[0],
                existing_table.column_count,
                candidate_table.column_count,
            )
            return 0.0

        # Calculate the baseline similarity using column signatures.
        signature_similarity = existing_table.get_similarity(candidate_table)

        bonus = 0.0

        # Add a bonus when both tables have identical non-empty headers.
        if existing_table.headers and existing_table.headers == candidate_table.headers:
            bonus += self.bonuses["headers"]

        # Add a bonus when both tables have identical non-empty header extras.
        if existing_table.headers_extras and existing_table.headers_extras == candidate_table.headers_extras:
            bonus += self.bonuses["headers_extras"]

        # Apply bonuses only to the remaining similarity gap.
        similarity = (
            signature_similarity
            + (1 - signature_similarity) * bonus
        )

        logger.debug(
            "Continuation similarity calculated\n"
            "  Existing logical table : Pages %s-%s\n"
            "  Current-page candidate : Page %s\n"
            "  Signature similarity   : %.4f\n"
            "  Header bonus            : %.4f\n"
            "  Final similarity        : %.4f",
            existing_table.pages[0],
            existing_table.pages[-1],
            candidate_table.pages[0],
            signature_similarity,
            bonus,
            similarity,
        )

        return similarity
