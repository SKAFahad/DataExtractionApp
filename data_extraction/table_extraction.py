import camelot
import fitz  # PyMuPDF
import pandas as pd
import re
import logging
from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TableExtractor:
    nPattern = r"[0-9]{1,3}(?:,[0-9]{3})+"  # Regex to identify numerical patterns

    def __init__(self, file_path):
        """
        Initialize the extractor with the file path.
        """
        self.file_path = file_path
        self.keywords = {
            "SOFP": ["financial position", "assets", "liabilities", "equity"],
            "SOPL": ["profit or loss", "revenue", "expense", "tax"],
            "SOCF": ["cash flows", "investing", "operating", "financing"]
        }

    def _read_pdf(self):
        """
        Read the PDF file using PyMuPDF.
        """
        try:
            return fitz.open(self.file_path)
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")
            return None

    def _extract_tables_from_pdf(self, page_no=None):
        """
        Extract tables from the specified page(s) of a PDF using Camelot.
        """
        try:
            tables = camelot.read_pdf(
                self.file_path,
                flavor="stream",
                pages=page_no if page_no else "all",
                edge_tol=150
            )
            return tables
        except Exception as e:
            logging.error(f"Error extracting tables from PDF: {e}")
            return None

    def _extract_tables_from_docx(self):
        """
        Extract tables from a DOCX file.
        """
        try:
            document = Document(self.file_path)
            tables = []
            for table in document.tables:
                data = []
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    data.append(row_data)
                df = pd.DataFrame(data)
                tables.append(df)
            return tables
        except Exception as e:
            logging.error(f"Error extracting tables from DOCX: {e}")
            return None

    def _clean_table(self, table):
        """
        Clean and format the extracted table.
        """
        # Drop columns with excessive NaNs
        table = table.dropna(axis=1, thresh=table.shape[0] * 0.5)

        # Drop rows with excessive NaNs
        table = table.dropna(axis=0, thresh=table.shape[1] * 0.5)

        # Reset column index
        table.columns = list(range(table.shape[1]))

        # Remove unnecessary characters
        table = table.applymap(lambda x: re.sub(r"\s+", " ", str(x)) if isinstance(x, str) else x)

        return table

    def extract_relevant_tables(self, type_):
        """
        Extract tables relevant to a specific financial report type.
        """
        if self.file_path.lower().endswith(".pdf"):
            document = self._read_pdf()
            if not document:
                return None

            page_match = {}
            for page_num, page in enumerate(document):
                text = page.get_text("text").lower()
                match_count = sum(1 for kw in self.keywords[type_] if kw in text)
                if match_count > 0:
                    page_match[page_num + 1] = match_count

            # Get page numbers with highest matches
            relevant_pages = sorted(page_match.keys(), key=lambda x: page_match[x], reverse=True)

            if not relevant_pages:
                logging.warning("No relevant pages found for the specified report type.")
                return None

            # Extract and clean tables from relevant pages
            extracted_tables = []
            for page_no in relevant_pages:
                tables = self._extract_tables_from_pdf(str(page_no))
                if tables:
                    for table in tables:
                        cleaned_table = self._clean_table(table.df)
                        extracted_tables.append(cleaned_table)

            return extracted_tables

        elif self.file_path.lower().endswith(".docx"):
            logging.info("Extracting tables from DOCX...")
            tables = self._extract_tables_from_docx()
            if tables:
                cleaned_tables = [self._clean_table(table) for table in tables]
                return cleaned_tables
            else:
                logging.warning("No tables found in the DOCX file.")
                return None
        else:
            logging.warning("Unsupported file format. Only PDF and DOCX are supported.")
            return None

    def save_tables(self, type_, output_folder):
        """
        Save extracted tables to the specified output folder.
        """
        tables = self.extract_relevant_tables(type_)
        if not tables:
            logging.warning(f"No tables found for type {type_}")
            return None

        for idx, table in enumerate(tables):
            output_path = f"{output_folder}/table_{type_}_{idx + 1}.csv"
            table.to_csv(output_path, index=False, encoding="utf-8-sig")
            logging.info(f"Saved table to {output_path}")


# Example Usage
if __name__ == "__main__":
    file_path = "path/to/your/document.pdf"  # Replace with your file path
    output_dir = "output/tables"

    extractor = TableExtractor(file_path)
    extractor.save_tables("SOFP", output_dir)
