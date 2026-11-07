
class PhysicalTable:
    """Represents a physical table extracted by Camelot."""

    def __init__(self, camelot_table):
        self._table = camelot_table
        self._data_start_index = 0
        self._headers = None
        self._headers_extras = []

    @property
    def table(self):
        return self._table

    @property
    def cells(self):
        return self._table.cells

    @property
    def data(self):
        return self._table.data

    @property
    def page(self):
        return self._table.page

    @property
    def row_count(self):
        return len(self.data)

    @property
    def column_count(self):
        return len(self.data[0]) if self.data else 0

    @property
    def data_start_index(self):
        return self._data_start_index

    @property
    def headers(self):
        if self._headers is None:
            self._headers = self.get_headers()
        return self._headers

    @property
    def headers_extras(self):
        return self._headers_extras

    @staticmethod
    def get_header_spans(row: list) -> list[int]:
        spans, width = [], 1

        for cell in row:
            width += not cell.right

            if cell.right:
                spans.append(width)
                width = 1

        return spans

    @staticmethod
    def normalize_text(text: str) -> str:
        return text.replace('\n', ' ').strip()

    @staticmethod
    def normalize_headers(headers: list[str]) -> list[str]:
        return [
            PhysicalTable.normalize_text(header)
            for header in headers
        ]

    @staticmethod
    def expand_headers(
        headers: list[str],
        spans: list[int],
    ) -> list[str]:
        expanded_headers = []
        index = 0

        for span in spans:
            expanded_headers.extend([headers[index]] * span)
            index += span

        return expanded_headers

    def get_headers(self) -> list[str]:

        # A single-row table contains data, not headers.
        if self.row_count == 1:
            return []

        headers = [""] * self.column_count

        for index, (cell_row, data_row) in enumerate(
            zip(self.cells, self.data)
        ):
            # Data starts immediately after the current header row.
            self._data_start_index = index + 1

            spans = self.get_header_spans(cell_row)

            # Skip a row whose header spans all columns.
            if len(spans) == 1:
                if headers_extra := self.normalize_text(data_row[0]):
                    self._headers_extras.append(headers_extra)
                continue

            expanded_headers = self.expand_headers(data_row, spans)

            # Combine this row with previously discovered header levels.
            headers = [
                f"{a} {b}".strip()
                for a, b in zip(headers, expanded_headers)
            ]

            # Stop once a clean single-level header is encountered.
            if len(spans) == sum(spans) == self.column_count:
                break

        return self.normalize_headers(headers)
