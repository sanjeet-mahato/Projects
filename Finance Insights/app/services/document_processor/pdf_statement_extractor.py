import logging
from io import BytesIO

import camelot

from app.services.document_processor.physical_table import PhysicalTable
from app.services.document_processor.logical_table import LogicalTable
from app.services.document_processor.logical_table_assembler import LogicalTableAssembler
from app.services.document_processor.cross_pdf_table_consolidator import CrossPDFTableConsolidator


logger = logging.getLogger(__name__)


class PDFStatementExtractor:
    """
    Orchestrates PDF extraction, logical table assembly, and
    cross-PDF table consolidation.
    """

    def __init__(self, pdfs: list[dict[str, str | bytes]]):
        if not pdfs:
            raise ValueError("At least one PDF must be provided.")

        self.pdfs = pdfs

        self.assembler = LogicalTableAssembler()
        self.consolidator = CrossPDFTableConsolidator()

        self.logical_tables_by_pdf: dict[str, list[LogicalTable]] = {}
        self.logical_tables: list[LogicalTable] = []

    def extract(self) -> list[LogicalTable]:
        """
        Extract logical tables from each PDF and consolidate
        structurally similar tables across PDFs.
        """

        logger.info(
            "Starting statement extraction | PDFs: %d",
            len(self.pdfs),
        )

        for pdf in self.pdfs:
            camelot_tables = camelot.read_pdf(
                BytesIO(pdf["content"]),
                pages="all",
                flavor="lattice",
                parallel=True,
                cpu_count=4,
            )

            physical_tables = [
                PhysicalTable(table, pdf["name"])
                for table in camelot_tables
            ]

            logical_tables = self.assembler.assemble(physical_tables)

            self.logical_tables_by_pdf[pdf["name"]] = logical_tables

            logger.info(
                "PDF processed | PDF: %s | Physical tables: %d | "
                "Logical tables: %d",
                pdf["name"],
                len(physical_tables),
                len(logical_tables),
            )

        self.logical_tables = self.consolidator.consolidate(
            self.logical_tables_by_pdf
        )

        logger.info(
            "Statement extraction completed | PDFs: %d | "
            "Consolidated tables: %d",
            len(self.pdfs),
            len(self.logical_tables),
        )

        return self.logical_tables
