from __future__ import annotations

import logging
from statistics import mean

import pandas as pd

from app.services.document_processor.column_signature import ColumnSignature


logger = logging.getLogger(__name__)


class LogicalTable:
    """Represents an independent logical table."""

    def __init__(self, physical_table):
        # Copy the headers and header extras from the physical table.
        self._headers = physical_table.headers.copy()
        self._headers_extras = physical_table.headers_extras.copy()

        # Keep only the data rows, excluding any rows identified as headers.
        self._data = [
            row.copy()
            for row in physical_table.data[
                physical_table.data_start_index:
            ]
        ]

        # Track the physical tables that contribute to this logical table.
        self._source_tables = [physical_table]

        # Initialize cached properties. They are created only when accessed.
        self._df = None
        self._signatures = None

    @property
    def headers(self) -> list[str]:
        """Return the column headers."""
        return self._headers

    @property
    def headers_extras(self) -> list[str]:
        """Return additional header information, such as full-width headings."""
        return self._headers_extras

    @property
    def data(self) -> list[list]:
        """Return the table's underlying row data."""
        return self._data

    @property
    def row_count(self) -> int:
        """Return the number of data rows."""
        return len(self._data)

    @property
    def column_count(self) -> int:
        """Derive the column count from the first data row."""
        return len(self._data[0]) if self._data else 0

    @property
    def source_tables(self) -> list:
        """Return all physical tables contributing to this logical table."""
        return self._source_tables

    @property
    def pages(self) -> list:
        """Return the page numbers of all contributing physical tables."""
        return [
            table.page
            for table in self._source_tables
        ]

    @property
    def df(self) -> pd.DataFrame:
        """Build the DataFrame only when first requested."""
        if self._df is None:
            self._df = pd.DataFrame(
                self._data,
                columns=self._headers if self._headers else None,
            )

        return self._df

    @property
    def signatures(self) -> list[ColumnSignature]:
        """Generate and cache a signature for each column when first requested."""
        if self._signatures is None:
            columns = zip(*self._data)

            self._signatures = [
                ColumnSignature(list(column))
                for column in columns
            ]

        return self._signatures

    def append_rows(self, rows: list[list]) -> None:
        """Append rows after validating their column count."""

        # Ensure every incoming row has the same number of columns.
        if any(len(row) != self.column_count for row in rows):
            logger.warning(
                "Cannot append rows | Logical table pages: %s-%s | "
                "Expected columns: %s",
                self.pages[0],
                self.pages[-1],
                self.column_count,
            )
            raise ValueError("Rows contain an unexpected number of columns.")

        # Copy the incoming rows to avoid sharing mutable row references.
        self._data.extend(row.copy() for row in rows)

        # Invalidate cached properties because the underlying data has changed.
        self._df = None
        self._signatures = None

    def append_table(self, table: LogicalTable) -> None:
        """Append another compatible logical table."""

        # Only tables with identical headers can be appended directly.
        if self.headers != table.headers:
            logger.warning(
                "Cannot append logical tables with different headers | "
                "Existing logical table pages: %s-%s | "
                "Current-page candidate: %s",
                self.pages[0],
                self.pages[-1],
                table.pages[0],
            )
            raise ValueError(
                "Cannot append tables with different headers."
            )

        # Append the incoming data and track its contributing physical tables.
        self.append_rows(table.data)
        self._source_tables.extend(table.source_tables)

    def get_similarity(self, candidate_table: LogicalTable) -> float:
        """Calculate average column-signature similarity."""

        existing_pages = f"{self.pages[0]}-{self.pages[-1]}"
        candidate_page = candidate_table.pages[0]

        # Tables with different column counts cannot be considered compatible.
        if self.column_count != candidate_table.column_count:
            logger.debug(
                "Column count mismatch | "
                "Existing logical table pages: %s | "
                "Current-page candidate: %s | "
                "Existing columns: %s | Candidate columns: %s",
                existing_pages,
                candidate_page,
                self.column_count,
                candidate_table.column_count,
            )
            return 0.0

        # Avoid calculating similarity when there are no columns to compare.
        if self.column_count == 0:
            return 0.0

        logger.debug(
            "Comparing table signatures\n"
            "  Existing logical table pages: %s\n"
            "  Current-page candidate: %s\n"
            "  Existing headers: %s\n"
            "  Candidate headers: %s",
            existing_pages,
            candidate_page,
            self.headers,
            candidate_table.headers,
        )

        # Compare corresponding column signatures.
        similarities = [
            existing_signature.compare(candidate_signature, column_index=index,)
            for index, (existing_signature, candidate_signature,) in enumerate(
                zip(self.signatures, candidate_table.signatures)
            )
        ]

        # Use the mean column similarity as the overall signature similarity.
        return mean(similarities)

    def update_headers(
        self,
        headers: list[str],
        headers_extras: list[str] | None = None,
        move_current_to_data: bool = False,
    ) -> None:
        """Update headers and optionally preserve the old headers as data."""

        # Preserve the existing headers as a data row when requested.
        if move_current_to_data and self._headers:
            self._data.insert(0, self._headers.copy())

        # Replace the headers and their additional information.
        self._headers = headers.copy()
        self._headers_extras = (headers_extras or []).copy()

        # Invalidate cached properties because the table structure has changed.
        self._df = None
        self._signatures = None

        logger.debug(
            "Logical table headers updated | Pages: %s-%s | "
            "Headers: %s | Header extras: %s",
            self.pages[0],
            self.pages[-1],
            self._headers,
            self._headers_extras,
        )
