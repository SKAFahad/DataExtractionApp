import argparse
import os
import logging
from data_extraction.text_extraction import extract_text_from_file
from data_extraction.image_extraction import extract_images_from_file
from data_extraction.table_extraction import TableExtractor
from data_extraction.relationship_mapping import map_and_save_relationships
from data_extraction.report_generation import generate_findings_report
from data_extraction.utils import ensure_output_folder
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default paths
DEFAULT_INPUT_FOLDER = os.path.join(os.path.dirname(__file__), "input")
DEFAULT_OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "output")

def process_file(input_path, output_folder):
    logging.info(f"Processing file: {input_path}")
    ensure_output_folder(output_folder)

    # Extract Text
    logging.info("Extracting text...")
    paragraphs_folder = os.path.join(output_folder, "paragraphs")
    text_data = extract_text_from_file(input_path, paragraphs_folder)
    if not text_data["text"]:
        logging.warning("No text extracted. Skipping.")
        return

    logging.info(f"Detected language: {text_data['language']}")
    logging.info(f"Named Entities: {text_data['entities']}")

    # Extract Images
    logging.info("Extracting images...")
    images_folder = os.path.join(output_folder, "images")
    ensure_output_folder(images_folder)
    images = extract_images_from_file(input_path, images_folder)

    # Extract Tables
    logging.info("Extracting tables...")
    tables_folder = os.path.join(output_folder, "tables")
    ensure_output_folder(tables_folder)

    table_extractor = TableExtractor(input_path)
    table_extractor.save_tables("SOFP", tables_folder)  # Statement of Financial Position
    table_extractor.save_tables("SOPL", tables_folder)  # Statement of Profit or Loss
    table_extractor.save_tables("SOCF", tables_folder)  # Statement of Cash Flows

    # Map Relationships
    logging.info("Mapping relationships...")
    relationships_folder = os.path.join(output_folder, "relationships")
    ensure_output_folder(relationships_folder)
    map_and_save_relationships(text_data["text"], images, [], relationships_folder)

    # Generate Findings Report
    logging.info("Generating findings report...")
    findings_folder = os.path.join(output_folder, "findings")
    ensure_output_folder(findings_folder)
    generate_findings_report(text_data["text"], images, [], findings_folder)

    logging.info(f"Processing completed for: {input_path}")

def main(input_folder, output_folder):
    ensure_output_folder(output_folder)
    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    if not input_files:
        logging.warning("No files found in the input folder. Exiting.")
        return

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_file,
                os.path.join(input_folder, file_name),
                os.path.join(output_folder, os.path.splitext(file_name)[0])
            )
            for file_name in input_files
        ]
        for future in futures:
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Extraction and Relationship Mapping Application')
    parser.add_argument('--input', default=DEFAULT_INPUT_FOLDER, help='Input folder location (path to the folder containing documents)')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_FOLDER, help='Output folder location (path to save outputs)')
    args = parser.parse_args()

    main(args.input, args.output)
