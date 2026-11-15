import logging
from collections import defaultdict

from app.services.apploadconfig import config
from app.services.document_processor.physical_table import PhysicalTable
from app.services.document_processor.logical_table import LogicalTable


logger = logging.getLogger(__name__)


class LogicalTableAssembler:
    """Combine physical tables into logical tables within a PDF."""

    def __init__(self):
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

    def assemble(
        self,
        physical_tables: list[PhysicalTable],
    ) -> list[LogicalTable]:
        """Assemble physical tables into logical tables."""

        logger.info(
            "Starting logical table assembly | Physical tables: %s",
            len(physical_tables),
        )

        # Group physical tables by their PDF page number.
        page_tables = self._group_tables_by_page(physical_tables)

        logical_tables: list[LogicalTable] = []
        previous_page_tables = []

        # Process pages in ascending order.
        for page_number in sorted(page_tables):

            # Create a logical table candidate for every physical table.
            current_page_candidates = [
                LogicalTable(physical_table)
                for physical_table in page_tables[page_number]
            ]

            # The first page has no previous tables to compare against.
            if not previous_page_tables:
                logical_tables.extend(current_page_candidates)
                previous_page_tables = current_page_candidates

                for candidate in current_page_candidates:
                    logger.info(
                        "New logical table created\n"
                        "  Sources :\n%s\n"
                        "  Columns : %s\n"
                        "  Rows    : %s",
                        candidate.pages_display,
                        candidate.column_count,
                        candidate.row_count,
                    )

                continue

            extended_tables, new_tables = self._process_page_tables(
                previous_page_tables,
                current_page_candidates,
                page_number,
            )

            logical_tables.extend(new_tables)

            # Only tables present on the current page are considered
            # for matching against the next page.
            previous_page_tables = extended_tables + new_tables

        logger.info(
            "Logical table assembly completed\n"
            "  Physical tables : %s\n"
            "  Logical tables  : %s",
            sum(len(tables) for tables in page_tables.values()),
            len(logical_tables),
        )

        return logical_tables

    @staticmethod
    def _group_tables_by_page(
        physical_tables: list[PhysicalTable],
    ) -> dict:
        """Group physical tables by page number."""

        page_tables = defaultdict(list)

        for physical_table in physical_tables:

            # Ignore tables without any extracted rows.
            if physical_table.row_count == 0:
                logger.debug(
                    "Skipping empty physical table | PDF: %s | Page: %s",
                    physical_table.pdf_name,
                    physical_table.page,
                )
                continue

            page_tables[physical_table.page].append(physical_table)

        # Report how many physical tables were found on each page.
        for page_number in sorted(page_tables):
            logger.info(
                "PDF: %s | Page %s | Found %s physical table(s)",
                page_tables[page_number][0].pdf_name,
                page_number,
                len(page_tables[page_number]),
            )

        return page_tables

    def _process_page_tables(
        self,
        previous_page_tables: list[LogicalTable],
        current_page_candidates: list[LogicalTable],
        page_number: int,
    ) -> tuple[list[LogicalTable], list[LogicalTable]]:
        """Match, merge, and identify logical tables on the current page."""

        # Find one-to-one matches with tables from the previous page.
        matches, new_tables = self._match_tables(
            previous_page_tables,
            current_page_candidates,
        )

        extended_tables = []

        # Merge matched candidates into their corresponding logical tables.
        for target, candidate in matches:

            # Reuse the target headers when the candidate headers differ.
            if candidate.headers != target.headers:
                candidate.update_headers(
                    headers=target.headers,
                    headers_extras=target.headers_extras,
                    move_current_to_data=bool(candidate.headers),
                )

            target.merge_table(candidate)

            logger.info(
                "Physical table merged into logical table\n"
                "  Current page  : %s\n"
                "  Logical table :\n%s\n"
                "  Rows added    : %s\n"
                "  Total rows    : %s",
                page_number,
                target.pages_display,
                candidate.row_count,
                target.row_count,
            )

            extended_tables.append(target)

        # Unmatched candidates represent new logical tables.
        for candidate in new_tables:
            logger.info(
                "New logical table created\n"
                "  Sources :\n%s\n"
                "  Columns : %s\n"
                "  Rows    : %s",
                candidate.pages_display,
                candidate.column_count,
                candidate.row_count,
            )

        return extended_tables, new_tables

    def _match_tables(
        self,
        previous_tables: list[LogicalTable],
        current_tables: list[LogicalTable],
    ) -> tuple[
        list[tuple[LogicalTable, LogicalTable]],
        list[LogicalTable],
    ]:
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

            matches.append((
                previous_tables[previous_index],
                current_tables[candidate_index],
            ))

            matched_previous.add(previous_index)
            matched_current.add(candidate_index)

            logger.debug(
                "Accepted table match\n"
                "  Existing logical table :\n%s\n"
                "  Current-page candidate :\n%s\n"
                "  Similarity             : %.4f",
                previous_tables[previous_index].pages_display,
                current_tables[candidate_index].pages_display,
                similarity,
            )

        # Identify current-page candidates that were not matched.
        new_tables = [
            table
            for index, table in enumerate(current_tables)
            if index not in matched_current
        ]

        return matches, new_tables

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
                "  Existing logical table :\n%s\n"
                "  Current-page candidate :\n%s\n"
                "  Existing columns       : %s\n"
                "  Candidate columns      : %s",
                existing_table.pages_display,
                candidate_table.pages_display,
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
            "  Existing logical table :\n%s\n"
            "  Current-page candidate :\n%s\n"
            "  Signature similarity   : %.4f\n"
            "  Header bonus            : %.4f\n"
            "  Final similarity        : %.4f",
            existing_table.pages_display,
            candidate_table.pages_display,
            signature_similarity,
            bonus,
            similarity,
        )

        return similarity
