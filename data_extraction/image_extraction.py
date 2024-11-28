import os
import fitz  # PyMuPDF
import zipfile
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_images_from_pdf(pdf_path, output_folder):
    image_paths = []
    try:
        pdf_file = fitz.open(pdf_path)
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            image_list = page.get_images(full=True)
            if image_list:
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_filename = f"image_page{page_index+1}_{img_index+1}.{image_ext}"
                    image_path = os.path.join(output_folder, image_filename)
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_bytes)
                    image_paths.append(image_path)
                    logging.info(f"Extracted image: {image_path}")
    except Exception as e:
        logging.error(f"Error extracting images from PDF: {e}")
    return image_paths

def extract_images_from_docx(docx_path, output_folder):
    image_paths = []
    try:
        with zipfile.ZipFile(docx_path, 'r') as docx_zip:
            for file_info in docx_zip.infolist():
                if file_info.filename.startswith('word/media/'):
                    image_ext = os.path.splitext(file_info.filename)[1]
                    image_data = docx_zip.read(file_info)
                    image_filename = os.path.basename(file_info.filename)
                    image_path = os.path.join(output_folder, image_filename)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_data)
                    image_paths.append(image_path)
                    logging.info(f"Extracted image: {image_path}")
    except Exception as e:
        logging.error(f"Error extracting images from DOCX: {e}")
    return image_paths

def extract_images_from_file(file_path, output_folder):
    if file_path.lower().endswith('.pdf'):
        return extract_images_from_pdf(file_path, output_folder)
    elif file_path.lower().endswith('.docx'):
        return extract_images_from_docx(file_path, output_folder)
    else:
        logging.warning("Unsupported file format for image extraction.")
        return []

def extract_images_from_files(file_paths, output_folder):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_images_from_file, file_path, output_folder) for file_path in file_paths]
        results = [future.result() for future in futures]
    return results
