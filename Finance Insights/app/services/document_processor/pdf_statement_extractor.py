
from collections import defaultdict
from pathlib import Path

import camelot

from app.services.apploadconfig import config
from app.services.document_processor.physical_table import PhysicalTable
from app.services.document_processor.logical_table import LogicalTable


class PDFStatementExtractor:
    """Extract physical PDF tables and combine them into logical tables."""

    def __init__(self, pdf_path: str | Path, pages: str = "all"):
        self.pdf_path = Path(pdf_path)
        self.pages = pages

        logical_config = config["logical_table"]

        self.similarity_threshold = float(
            logical_config["similarity_threshold"]
        )

        self.bonuses = {
            "headers": float(logical_config["header_bonus"]),
            "headers_extras": float(
                logical_config["headers_extras_bonus"]
            ),
        }

        if any(bonus < 0 for bonus in self.bonuses.values()):
            raise ValueError("Similarity bonuses cannot be negative.")

        if sum(self.bonuses.values()) > 1:
            raise ValueError("Combined similarity bonuses cannot exceed 1.")

        if not 0 <= self.similarity_threshold <= 1:
            raise ValueError("Similarity threshold must be between 0 and 1.")

        self.logical_tables: list[LogicalTable] = []

    def extract(self) -> list[LogicalTable]:
        """Extract and combine tables from the PDF."""

        camelot_tables = camelot.read_pdf(
            str(self.pdf_path),
            pages=self.pages,
            flavor="lattice",
        )

        page_tables = defaultdict(list)

        for camelot_table in camelot_tables:
            physical_table = PhysicalTable(camelot_table)

            if physical_table.row_count == 0:
                continue

            page_tables[physical_table.page].append(physical_table)

        self.logical_tables = []
        previous_page_tables = []

        for page_number in sorted(page_tables):
            candidates = [
                LogicalTable(physical_table)
                for physical_table in page_tables[page_number]
            ]

            if not previous_page_tables:
                self.logical_tables.extend(candidates)
                previous_page_tables = candidates
                continue

            matches = self._match_tables(
                previous_page_tables,
                candidates,
            )

            current_page_tables = []
            matched_candidates = set()

            for previous_index, candidate_index in matches:
                target = previous_page_tables[previous_index]
                candidate = candidates[candidate_index]

                if candidate.headers != target.headers:
                    candidate.update_headers(
                        headers=target.headers,
                        headers_extras=target.headers_extras,
                        move_current_to_data=bool(candidate.headers),
                    )

                target.append_table(candidate)

                current_page_tables.append(target)
                matched_candidates.add(candidate_index)

            for index, candidate in enumerate(candidates):
                if index not in matched_candidates:
                    self.logical_tables.append(candidate)
                    current_page_tables.append(candidate)

            previous_page_tables = current_page_tables

        return self.logical_tables

    def _match_tables(
        self,
        previous_tables: list[LogicalTable],
        current_tables: list[LogicalTable],
    ) -> list[tuple[int, int]]:
        """Find one-to-one matches between consecutive pages."""

        possible_matches = []

        for previous_index, previous_table in enumerate(previous_tables):
            for current_index, current_table in enumerate(current_tables):
                similarity = self._get_similarity(
                    previous_table,
                    current_table,
                )

                if similarity >= self.similarity_threshold:
                    possible_matches.append(
                        (similarity, previous_index, current_index)
                    )

        possible_matches.sort(
            key=lambda match: match[0],
            reverse=True,
        )

        matched_previous = set()
        matched_current = set()
        matches = []

        for _, previous_index, current_index in possible_matches:
            if previous_index in matched_previous:
                continue

            if current_index in matched_current:
                continue

            matches.append((previous_index, current_index))

            matched_previous.add(previous_index)
            matched_current.add(current_index)

        return matches

    def _get_similarity(
        self,
        left: LogicalTable,
        right: LogicalTable,
    ) -> float:
        """Calculate signature similarity with exact-match bonuses."""

        if left.column_count != right.column_count:
            return 0.0


        signature_similarity = left.get_similarity(right)

        bonus = 0.0

        if left.headers and left.headers == right.headers:
            bonus += self.bonuses["headers"]

        if left.headers_extras and left.headers_extras == right.headers_extras:
            bonus += self.bonuses["headers_extras"]

        return (
            signature_similarity
            + (1 - signature_similarity) * bonus
        )
