import logging

from app.services.apploadconfig import config
from app.services.document_processor.logical_table import LogicalTable


logger = logging.getLogger(__name__)


class CrossPDFTableConsolidator:
    def __init__(self):
        self._similarity_threshold = float(config["logical_table"]["similarity_threshold"])

    def consolidate(
        self,
        logical_tables_by_pdf: dict[str, list[LogicalTable]],
    ) -> list[LogicalTable]:
        """
        Group similar logical tables across PDFs and consolidate each group.
        Each group produces exactly one consolidated table.
        """
        groups = self._create_groups(logical_tables_by_pdf)
        consolidated_tables = []

        logger.info(
            "Cross-PDF consolidation started | PDFs: %d | Tables: %d | Groups: %d",
            len(logical_tables_by_pdf),
            sum(len(tables) for tables in logical_tables_by_pdf.values()),
            len(groups),
        )

        for group in groups:
            consolidated_table = self._consolidate_group(group)
            consolidated_tables.append(consolidated_table)

            logger.info(
                "Group consolidated | Input tables: %d | Final rows: %d",
                len(group),
                consolidated_table.row_count,
            )

        return consolidated_tables

    # ------------------------------------------------------------------
    # GROUPING
    # ------------------------------------------------------------------

    def _create_groups(
        self,
        logical_tables_by_pdf: dict[str, list[LogicalTable]],
    ) -> list[list[tuple[str, LogicalTable]]]:
        """
        Group structurally similar logical tables across different PDFs.
        Each group can contain at most one logical table from each PDF.
        """
        groups = []

        for pdf_name, tables in logical_tables_by_pdf.items():
            matches = []

            # Find all valid table-to-group matches for the current PDF.
            for table_index, table in enumerate(tables):
                for group_index, group in enumerate(groups):
                    score = self._get_group_match_score(pdf_name, table, group)

                    if score is not None:
                        matches.append((score, table_index, group_index))

            # Process the strongest matches first, preserving input order for ties.
            matches.sort(key=lambda match: (-match[0], match[1], match[2]))

            assigned_tables = set()
            assigned_groups = set()

            # Assign each table and group at most once for this PDF.
            for _, table_index, group_index in matches:
                if table_index in assigned_tables or group_index in assigned_groups:
                    continue

                groups[group_index].append((pdf_name, tables[table_index]))

                assigned_tables.add(table_index)
                assigned_groups.add(group_index)

            # Tables without a matching group start new groups.
            for table_index, table in enumerate(tables):
                if table_index not in assigned_tables:
                    groups.append([(pdf_name, table)])

        return groups

    def _get_group_match_score(
        self,
        pdf_name: str,
        table: LogicalTable,
        group: list[tuple[str, LogicalTable]],
    ) -> float | None:
        """
        Check whether a table is compatible with a group.

        Return the minimum similarity score across group members,
        or None when the table does not qualify.
        """
        # A group cannot contain multiple tables from the same PDF.
        if any(existing_pdf == pdf_name for existing_pdf, _ in group):
            return None

        # Headers must exist and match exactly.
        if not table.headers or table.headers != group[0][1].headers:
            return None

        # The incoming table must meet the threshold against every group member.
        similarity = min(
            table.get_similarity(existing_table)
            for _, existing_table in group
        )

        if similarity < self._similarity_threshold:
            return None

        return similarity

    # ------------------------------------------------------------------
    # CONSOLIDATION
    # ------------------------------------------------------------------

    @staticmethod
    def _consolidate_group(
        group: list[tuple[str, LogicalTable]],
    ) -> LogicalTable:
        """
        Iteratively consolidate overlapping and contained logical tables.

        Initially, every logical table is treated as an independent block.
        Each pair of blocks is checked for:
        1. Complete containment.
        2. Continuation overlap in either direction.

        After a successful operation, comparisons restart from the beginning.
        This allows newly merged blocks to be compared against every remaining
        block.

        Once all overlaps and containment relationships are resolved,
        any remaining blocks are concatenated into a single logical table.
        """
        blocks = [table for _, table in group]
        changed = True

        while changed:
            changed = False

            for first_index in range(len(blocks)):
                for second_index in range(first_index + 1, len(blocks)):
                    first = blocks[first_index]
                    second = blocks[second_index]

                    # If the second block is already present in the first,
                    # discard the redundant block.
                    if first.contains(second):
                        blocks.pop(second_index)
                        changed = True
                        break

                    # If the first block is already present in the second,
                    # discard the first block and retain the second.
                    if second.contains(first):
                        blocks.pop(first_index)
                        changed = True
                        break

                    # Check whether the first block precedes the second.
                    if overlap := first.find_continuation_overlap(second):
                        first.merge_table(second, overlap_length=overlap)
                        blocks.pop(second_index)
                        changed = True
                        break

                    # Check whether the second block precedes the first.
                    if overlap := second.find_continuation_overlap(first):
                        second.merge_table(first, overlap_length=overlap)
                        blocks.pop(first_index)
                        changed = True
                        break

                # Restart comparisons after every successful operation.
                if changed:
                    break

        # Combine any remaining non-overlapping blocks.
        consolidated_table = blocks[0]

        for block in blocks[1:]:
            consolidated_table.merge_table(block)

        return consolidated_table
