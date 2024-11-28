import fitz  # PyMuPDF
import textract
import docx2txt
from langdetect import detect
import spacy
import logging
import os
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load SpaCy model for NER
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text += page_text
            else:
                logging.warning(f"No text found on page {page_num + 1}")
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        text = docx2txt.process(docx_path)
        if not text:
            logging.warning("No text extracted from DOCX file.")
    except Exception as e:
        logging.error(f"Error extracting text from DOCX: {e}")
    return text

def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "unknown"

def perform_ner(text):
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        logging.error(f"Error performing NER: {e}")
        return []

def save_paragraphs_to_folder(text, output_folder):
    """
    Save each paragraph in the text to a separate file in the specified folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    paragraphs = text.split("\n\n")  # Split text into paragraphs
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():  # Ensure paragraph is not empty
            paragraph_filename = f"paragraph_{i+1}.txt"
            paragraph_path = os.path.join(output_folder, paragraph_filename)
            with open(paragraph_path, 'w', encoding='utf-8') as file:
                file.write(paragraph)
            logging.info(f"Saved paragraph {i+1} to {paragraph_path}")

def extract_text_from_file(file_path, output_folder):
    text = ""
    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        try:
            text_bytes = textract.process(file_path)
            text = text_bytes.decode('utf-8')
        except Exception as e:
            logging.error(f"Error extracting text from file: {e}")

    if not text:
        logging.warning(f"No text extracted from file: {file_path}")
    else:
        logging.info(f"Extracted text from file: {file_path}")

    language = detect_language(text)
    entities = perform_ner(text)

    # Save paragraphs to folder
    paragraphs_folder = os.path.join(output_folder, "paragraphs")
    save_paragraphs_to_folder(text, paragraphs_folder)

    return {
        "text": text,
        "language": language,
        "entities": entities
    }

def extract_texts_from_files(file_paths, output_folder):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_text_from_file, file_path, output_folder) for file_path in file_paths]
        results = [future.result() for future in futures]
    return results

# Example usage
if __name__ == "__main__":
    file_paths = ["path/to/your/pdf_file.pdf", "path/to/your/docx_file.docx"]
    output_folder = "path/to/output/folder"
    extracted_texts = extract_texts_from_files(file_paths, output_folder)
    for extracted in extracted_texts:
        print(extracted)
