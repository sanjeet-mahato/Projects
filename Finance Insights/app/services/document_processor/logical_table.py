from __future__ import annotations
from statistics import mean

import pandas as pd

from app.services.document_processor.column_signature import ColumnSignature


class LogicalTable:
    """Represents an independent logical table."""

    def __init__(self, physical_table):
        self._headers = physical_table.headers.copy()
        self._headers_extras = physical_table.headers_extras.copy()

        self._data = [
            row.copy()
            for row in physical_table.data[
                physical_table.data_start_index:
            ]
        ]

        self._source_tables = [physical_table]

        self._df = None
        self._signatures = None

    @property
    def headers(self) -> list[str]:
        return self._headers

    @property
    def headers_extras(self) -> list[str]:
        return self._headers_extras

    @property
    def data(self) -> list[list]:
        return self._data

    @property
    def row_count(self) -> int:
        return len(self._data)

    @property
    def column_count(self) -> int:
        return len(self._data[0]) if self._data else 0

    @property
    def source_tables(self) -> list:
        return self._source_tables

    @property
    def pages(self) -> list:
        return [
            table.page
            for table in self._source_tables
        ]

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self._df = pd.DataFrame(
                self._data,
                columns=self._headers if self._headers else None,
            )

        return self._df

    @property
    def signatures(self) -> list[ColumnSignature]:
        if self._signatures is None:
            columns = zip(*self._data)

            self._signatures = [
                ColumnSignature(list(column))
                for column in columns
            ]

        return self._signatures

    def append_rows(self, rows: list[list]) -> None:
        """Append rows after validating their column count."""

        if any(len(row) != self.column_count for row in rows):
            raise ValueError("Rows contain an unexpected number of columns.")

        self._data.extend(row.copy() for row in rows)

        self._df = None
        self._signatures = None

    def append_table(self, table: LogicalTable) -> None:
        """Append another compatible logical table."""

        if self.headers != table.headers:
            raise ValueError(
                "Cannot append tables with different headers."
            )

        self.append_rows(table.data)
        self._source_tables.extend(table.source_tables)

    def get_similarity(self, table: LogicalTable) -> float:
        """Calculate average column-signature similarity."""

        if self.column_count != table.column_count:
            return 0.0

        if self.column_count == 0:
            return 0.0

        similarities = [
            left.compare(right)
            for left, right in zip(
                self.signatures,
                table.signatures,
            )
        ]

        return mean(similarities)

    def update_headers(
        self,
        headers: list[str],
        headers_extras: list[str] | None = None,
        move_current_to_data: bool = False,
    ) -> None:

        if move_current_to_data and self._headers:
            self._data.insert(0, self._headers.copy())

        self._headers = headers.copy()
        self._headers_extras = (headers_extras or []).copy()

        self._df = None
        self._signatures = None
