import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
from langdetect import detect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load T5 model for summarization and caption generation
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

def generate_summary(text, task="summarize"):
    """
    Generate a summary or caption using the T5 model.

    Args:
        text (str): Input text.
        task (str): Task type, e.g., "summarize" or "generate caption".

    Returns:
        str: Generated summary or caption.
    """
    try:
        input_text = f"{task}: {text}"
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(input_ids, num_beams=4, max_length=50, early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error generating {task}: {e}")
        return "No Summary Available"

def generate_image_caption(image_path):
    """
    Generate a caption for an image (Placeholder: Text-based processing).

    Args:
        image_path (str): Path to the image.

    Returns:
        str: Generated caption.
    """
    # Placeholder logic for generating captions based on image name or metadata
    image_name = os.path.basename(image_path)
    caption = generate_summary(f"This is an image named {image_name}", task="generate caption")
    return caption

def summarize_table(table_path):
    """
    Summarize the contents of a table.

    Args:
        table_path (str): Path to the CSV table file.

    Returns:
        str: Generated summary of the table.
    """
    try:
        df = pd.read_csv(table_path)
        table_text = df.to_string(index=False)
        return generate_summary(table_text, task="summarize")
    except Exception as e:
        logging.error(f"Error summarizing table: {e}")
        return "No Summary Available"

def save_report_for_finding(output_path, findings):
    """
    Save a report for each finding in the findings dictionary.

    Args:
        output_path (str): Path to save the report.
        findings (dict): Dictionary containing findings to save.
    """
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 50, "Findings Report")

        y_position = height - 80
        c.setFont("Helvetica", 12)

        for finding_type, details in findings.items():
            if y_position < 100:
                c.showPage()
                y_position = height - 50

            c.drawString(50, y_position, f"{finding_type.capitalize()}:")
            y_position -= 20

            for detail in details:
                c.drawString(70, y_position, detail)
                y_position -= 20

        c.save()
        logging.info(f"Report saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving findings report: {e}")

def generate_findings_report(text, images, tables, output_folder):
    """
    Generate a findings report based on text, images, and tables.

    Args:
        text (str): Extracted text from the document.
        images (list): List of image paths.
        tables (list): List of table paths.
        output_folder (str): Folder to save the findings report.

    Returns:
        None
    """
    findings = {
        "images": [],
        "tables": []
    }

    # Generate captions for images
    for image_path in images:
        caption = generate_image_caption(image_path)
        findings["images"].append(f"Image: {os.path.basename(image_path)}, Caption: {caption}")

    # Summarize tables and match with text
    for table_path in tables:
        table_summary = summarize_table(table_path)
        if "table" in text.lower():
            findings["tables"].append(f"Table: {os.path.basename(table_path)}, Summary: {table_summary}, Related Text: Found a matching text chunk mentioning a table.")

    # Save findings to a PDF report
    output_path = os.path.join(output_folder, "findings_report.pdf")
    save_report_for_finding(output_path, findings)

# Example Usage
if __name__ == "__main__":
    example_text = "This document contains important details in Table 1 and Figure 1."
    example_images = ["path/to/image1.png", "path/to/image2.png"]
    example_tables = ["path/to/table1.csv", "path/to/table2.csv"]
    output_dir = "path/to/output"

    generate_findings_report(example_text, example_images, example_tables, output_dir)
