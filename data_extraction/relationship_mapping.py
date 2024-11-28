import re
import os
import spacy
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load SpaCy model for NER
nlp = spacy.load('en_core_web_sm')

def map_relationships(text, images, tables):
    """
    Map relationships between text, images, and tables using NLP.

    Args:
        text (str): The extracted text from the document.
        images (list): List of image paths.
        tables (list): List of table paths.

    Returns:
        dict: A dictionary mapping text to images and tables.
    """
    relationships = {
        "text_to_images": {},
        "text_to_tables": {}
    }
    try:
        # Use spaCy to process the text
        doc = nlp(text)

        # Example references for images and tables
        for image in images:
            # Example: Match keywords like "Figure" or "Image" with some heuristic
            if "figure" in text.lower() or "image" in text.lower():
                relationships["text_to_images"][os.path.basename(image)] = "Mentioned in text"

        for table in tables:
            # Example: Match keywords like "Table"
            if "table" in text.lower():
                relationships["text_to_tables"][os.path.basename(table)] = "Mentioned in text"

        logging.info(f"Mapped relationships: {relationships}")

    except Exception as e:
        logging.error(f"Error mapping relationships: {e}")

    return relationships


def save_relationships_to_pdf(relationships, output_folder):
    """
    Save text-to-image and text-to-table relationships in separate PDFs.

    Args:
        relationships (dict): The relationships dictionary.
        output_folder (str): Output folder to save PDFs.
    """
    text_to_images_folder = os.path.join(output_folder, "text_to_images")
    text_to_tables_folder = os.path.join(output_folder, "text_to_tables")

    os.makedirs(text_to_images_folder, exist_ok=True)
    os.makedirs(text_to_tables_folder, exist_ok=True)

    # Save text-to-image relationships
    text_to_images_pdf = os.path.join(text_to_images_folder, "text_to_images.pdf")
    save_pdf(relationships["text_to_images"], text_to_images_pdf)
    logging.info(f"Saved text-to-image relationships to {text_to_images_pdf}")

    # Save text-to-table relationships
    text_to_tables_pdf = os.path.join(text_to_tables_folder, "text_to_tables.pdf")
    save_pdf(relationships["text_to_tables"], text_to_tables_pdf)
    logging.info(f"Saved text-to-table relationships to {text_to_tables_pdf}")


def save_pdf(content, pdf_path):
    """
    Create a PDF document for the given content.

    Args:
        content (dict): Dictionary to save in the PDF.
        pdf_path (str): Path to save the PDF.
    """
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 50, "Relationship Mapping")

        y_position = height - 80
        c.setFont("Helvetica", 12)

        for key, value in content.items():
            if y_position < 50:
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, f"{key}: {value}")
            y_position -= 20

        c.save()
    except Exception as e:
        logging.error(f"Error creating PDF: {e}")


def map_and_save_relationships(text, images, tables, output_folder):
    """
    Map relationships and save them to PDFs.

    Args:
        text (str): Extracted text from the document.
        images (list): List of extracted image paths.
        tables (list): List of extracted table paths.
        output_folder (str): Folder to save the PDFs.
    """
    relationships = map_relationships(text, images, tables)
    save_relationships_to_pdf(relationships, output_folder)


# Example Usage
if __name__ == "__main__":
    example_text = "This document contains Figure 1 and Table 2."
    example_images = ["path/to/image1.png", "path/to/image2.png"]
    example_tables = ["path/to/table1.csv", "path/to/table2.csv"]
    output_dir = "path/to/output"

    map_and_save_relationships(example_text, example_images, example_tables, output_dir)
