import logging
import os
import pandas as pd
from docx import Document
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the pre-trained DocTR model
model = ocr_predictor(pretrained=True)

def extract_tables_from_pdf(pdf_path, output_folder):
    table_paths = []
    try:
        # Load the PDF document
        doc = DocumentFile.from_pdf(pdf_path)
        # Perform OCR
        result = model(doc)
        # Extract tables from the OCR result
        for page_idx, page in enumerate(result.pages):
            for block in page.blocks:
                if block.type == 'table':
                    table_data = []
                    for row in block.rows:
                        table_data.append([cell.content for cell in row.cells])
                    df = pd.DataFrame(table_data)
                    table_filename = f"table_page{page_idx+1}_{len(table_paths)+1}.csv"
                    table_path = os.path.join(output_folder, table_filename)
                    df.to_csv(table_path, index=False, header=False)
                    table_paths.append(table_path)
                    logging.info(f"Extracted table: {table_path}")
    except Exception as e:
        logging.error(f"Error extracting tables from PDF: {e}")
    return table_paths

def extract_tables_from_docx(docx_path, output_folder):
    table_paths = []
    try:
        document = Document(docx_path)
        for idx, table in enumerate(document.tables):
            data = []
            for row in table.rows:
                text = [cell.text.strip() for cell in row.cells]
                data.append(text)
            df = pd.DataFrame(data)
            table_filename = f"table_{idx+1}.csv"
            table_path = os.path.join(output_folder, table_filename)
            df.to_csv(table_path, index=False, header=False)
            table_paths.append(table_path)
            logging.info(f"Extracted table: {table_path}")
    except Exception as e:
        logging.error(f"Error extracting tables from DOCX: {e}")
    return table_paths

def extract_tables_from_file(file_path, output_folder):
    if file_path.lower().endswith('.pdf'):
        return extract_tables_from_pdf(file_path, output_folder)
    elif file_path.lower().endswith('.docx'):
        return extract_tables_from_docx(file_path, output_folder)
    else:
        logging.warning("Unsupported file format for table extraction.")
        return []

def extract_tables_from_files(file_paths, output_folder):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_tables_from_file, file_path, output_folder) for file_path in file_paths]
        results = [future.result() for future in futures]
    return results

# Example usage
if __name__ == "__main__":
    pdf_path = "path/to/your/pdf_file.pdf"
    docx_path = "path/to/your/docx_file.docx"
    output_folder = "path/to/output/folder"
    extract_tables_from_pdf(pdf_path, output_folder)
    extract_tables_from_docx(docx_path, output_folder)