
# DataExtractionApp

A comprehensive Python-based application for extracting, processing, and analyzing data from PDF and DOCX documents. This app integrates advanced features for text extraction, table processing, image analysis, relationship mapping, and report generation, making it ideal for financial reports and other structured documents.


---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Dependencies](#dependencies)
6. [Python Libraries and Their Roles](#python-libraries-and-their-roles)
7. [Machine Learning Models and LLMs](#machine-learning-models-and-llms)
8. [Project Structure](#project-structure)
9. [Examples](#examples)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact](#contact)
13. [FAQ](#faq)
14. [Future Enhancements](#future-enhancements)
15. [Changelog](#changelog)

---

## Introduction

**DataExtractionApp** is a modular and extensible solution for analyzing structured documents. It supports:
- Extracting text and identifying linguistic entities.
- Processing tables from both PDFs and DOCX files.
- Generating captions and summarizing images.
- Mapping relationships between text, tables, and images.
- Producing structured reports summarizing extracted insights.

---

## Features

- **Text Extraction**:
  - Paragraph-level extraction with language detection.
  - Named Entity Recognition (NER) for advanced linguistic insights.

- **Table Processing**:
  - Extracts tables from PDFs using Camelot.
  - Processes tables from DOCX files using python-docx.
  - Cleans and formats extracted tables.
  - Supports financial reports like SOFP (Statement of Financial Position), SOPL (Profit or Loss), and SOCF (Cash Flows).

- **Image Analysis**:
  - Extracts and compresses images from documents.
  - Generates captions using NLP models.

- **Relationship Mapping**:
  - Maps relationships between text, tables, and images.
  - Saves mappings in organized PDF reports.

- **Report Generation**:
  - Summarizes findings in structured PDF reports.
  - Ensures file sizes are optimized for easy sharing.

- **Multi-File Support**:
  - Processes both PDF and DOCX files.

---

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **Git** for version control
- **Java** (required for `tabula-py` to extract tables from PDFs)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SKAFahad/DataExtractionApp.git
   cd DataExtractionApp
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

---

## Usage

### Command-Line Execution

Run the application using the following command:

```bash
python main.py --input "path/to/input/folder" --output "path/to/output/folder"
```

### Example
```bash
python main.py --input "samples" --output "results"
```

This processes all files in the `samples` directory and saves the results in the `results` directory.

---

## Dependencies

Key dependencies include:
- **PyPDF2**: For PDF text extraction.
- **textract**: To handle text extraction from various formats.
- **docx2txt**: For extracting text from DOCX files.
- **pandas**: For handling tabular data.
- **PyMuPDF (fitz)**: For PDF and image processing.
- **Camelot**: For extracting tables from PDFs.
- **python-docx**: For extracting tables from DOCX files.
- **transformers**: For text summarization and captioning.
- **torch**: For deep learning tasks.
- **reportlab**: For generating PDF reports.
- **tqdm**: For progress bars in the command-line interface.

---

## Python Libraries and Their Roles

### Core Libraries
- **`os`**: Handles file system interactions like directory creation and path management.
- **`logging`**: Tracks application events and errors for debugging.
- **`argparse`**: Parses command-line arguments for dynamic input/output specification.
- **`re`**: Provides regular expression matching for text and pattern extraction.

### Text and Document Processing
- **PyPDF2**: Extracts text from PDFs.
- **textract**: Supports text extraction from various document types (e.g., PDFs, DOCX).
- **docx2txt**: Handles text parsing from DOCX files.
- **python-docx**: Extracts tables from DOCX documents.

### Table Processing
- **pandas**: Manages and processes tabular data efficiently.
- **Camelot**: Extracts tables from PDFs using stream or lattice parsing methods.

### Image Processing
- **PyMuPDF (fitz)**: Extracts images and metadata from PDFs.
- **Pillow**: Handles image compression and optimization.

### NLP and Machine Learning
- **spacy**: Performs named entity recognition (NER) and linguistic analysis.
- **transformers**: Enables tasks like text summarization and image captioning using pre-trained large language models (LLMs).
- **torch**: Powers LLM computations for tasks such as summarization and text-to-table mapping.
- **langdetect**: Detects the language of extracted text.

### Reporting and Visualization
- **reportlab**: Creates findings reports and visual outputs as PDFs.
- **tabula-py**: Parses tables from PDFs requiring Java-based processing.

### Utilities
- **tqdm**: Adds progress bars for command-line operations.
- **sentencepiece**: Tokenizes inputs for transformer-based models.

---

## Machine Learning Models and LLMs

### 1. **Pre-trained Models from `transformers` Library**
- **Model Used**: T5 (Text-to-Text Transfer Transformer)
- **Role**:
  - **Image Captioning**: Generates meaningful captions for extracted images.
  - **Text Summarization**: Condenses extracted text and table data into concise insights.
  - **Text-to-Table Mapping**: Connects textual references with tables for contextual analysis.

---

## Project Structure

```
DataExtractionApp/
├── data_extraction/
│   ├── __init__.py
│   ├── text_extraction.py
│   ├── image_extraction.py
│   ├── table_extraction.py
│   ├── relationship_mapping.py
│   ├── report_generation.py
│   └── utils.py
├── main.py
├── requirements.txt
├── README.md
```

---

## FAQ

### 1. What file formats are supported?
PDF and DOCX files are supported for text, table, and image extraction.

### 2. How are large files handled?
Large files are processed efficiently by splitting tasks into smaller components and compressing images. Tables and text are extracted incrementally to manage memory effectively.

### 3. Do I need a GPU for this app?
A GPU is not mandatory but can improve performance for NLP and deep learning tasks.

---

## Future Enhancements

- Support for additional file formats like XLSX and HTML.
- Advanced NLP capabilities for better summarization.
- A GUI interface for non-technical users.

---

## Changelog

### v2.1.0
- Added dynamic handling of both PDF and DOCX files.
- Improved table extraction for financial reports.
- Enhanced relationship mapping and report generation.
