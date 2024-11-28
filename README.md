# DataExtractionApp

An application for automated extraction of text, images, and tables from documents (PDF and DOCX), mapping relationships using local NLP models, and generating structured PDF reports with contextually relevant titles.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)
- [FAQ](#frequently-asked-questions-faq)
- [Future Enhancements](#future-enhancements)
- [Project Status](#project-status)
- [Changelog](#changelog)

---

## Introduction

**DataExtractionApp** is a Python-based application designed to automate the extraction of textual content, images, and tables from documents in PDF and DOCX formats. Utilizing local Natural Language Processing (NLP) models, it maps relationships between these data elements and generates organized PDF reports with contextually relevant titles. The application is modular, ensuring ease of maintenance and scalability.

---

## Features

- **Text Extraction**: Extracts text from PDF and DOCX files while preserving structure.
- **Image Extraction**: Retrieves images and charts embedded in documents.
- **Table Extraction**: Identifies and extracts tables, saving them in CSV format.
- **Relationship Mapping**: Uses local NLP models to map references between text, images, and tables.
- **Report Generation**: Compiles extracted data into a structured PDF report with a generated title.
- **Modular Design**: Organized codebase with individual modules for each task.
- **Local NLP Models**: Ensures data privacy by processing data locally without external API calls.
- **GPU Acceleration**: Utilizes GPU resources for enhanced performance (if available).

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

- **data_extraction/**: Package containing modules for each data extraction task.
  - **text_extraction.py**: Functions to extract text from documents.
  - **image_extraction.py**: Functions to extract images from documents.
  - **table_extraction.py**: Functions to extract tables from documents.
  - **relationship_mapping.py**: Functions to map relationships using NLP.
  - **report_generation.py**: Functions to generate the final PDF report.
  - **utils.py**: Utility functions used across the application.
- **main.py**: Central script that orchestrates the execution of all modules.
- **requirements.txt**: List of all Python packages required by the application.
- **README.md**: Project documentation (this file).

---

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed on your system.
- **Git**: For cloning the repository.
- **Java**: Required for `tabula-py` to extract tables from PDFs.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SKAFahad/DataExtractionApp.git
   cd DataExtractionApp
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows (PowerShell)**:

     ```bash
     venv\Scripts\Activate.ps1
     ```

     If you encounter an execution policy error, run:

     ```bash
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

   - **Windows (Command Prompt)**:

     ```bash
     venv\Scriptsctivate.bat
     ```

   - **Linux/MacOS**:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Download spaCy Language Model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

---

## Usage

### Command-Line Execution

Run the application using the command line by specifying the input file and output folder.

```bash
python main.py --input "path/to/input/file.pdf" --output "path/to/output/folder"
```

### Example

```bash
python main.py --input "samples/sample_document.pdf" --output "output"
```

### Arguments

- `--input`: (Required) Path to the input PDF or DOCX file.
- `--output`: (Required) Path to the directory where outputs will be saved.

---

## Dependencies

The application relies on several Python libraries, which are listed in `requirements.txt`. Key dependencies include:

- **PyPDF2**: For PDF text extraction.
- **textract**: For text extraction from various file formats.
- **docx2txt**: For DOCX text extraction.
- **PyMuPDF (fitz)**: For image extraction from PDFs.
- **tabula-py**: For table extraction from PDFs (requires Java).
- **pandas**: For data manipulation and CSV handling.
- **numpy**: For numerical operations.
- **transformers**: For NLP tasks (e.g., summarization).
- **torch**: For running PyTorch models.
- **spaCy**: For advanced NLP tasks.
- **python-docx**: For DOCX table extraction.
- **reportlab**: For generating PDF reports.
- **Pillow**: For image processing.

---

## Examples

### Sample Input and Output

- **Input File**: A PDF or DOCX document containing text, images, and tables.
- **Output Folder**: The application will create the following in the specified output folder:
  - **final_report.pdf**: The generated PDF report.
  - **images/**: Folder containing extracted images.
  - **tables/**: Folder containing extracted tables in CSV format.

### Sample Execution

```bash
python main.py --input "samples/financial_report.pdf" --output "reports/financial_report_output"
```

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page to create a copy in your GitHub account.

2. **Clone the Forked Repository**

   ```bash
   git clone https://github.com/SKAFahad/DataExtractionApp.git
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   - Ensure code is well-commented and follows Python coding standards.
   - Test your changes thoroughly.

5. **Commit and Push**

   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

   - Go to the original repository on GitHub.
   - Click on "Pull Requests" and then "New Pull Request".
   - Select your branch and submit the pull request for review.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **OpenAI GPT-3.5**: For providing language models that inspire the NLP components.
- **spaCy**: For their powerful NLP library.
- **PyTorch**: For enabling efficient model computations.
- **The Python Community**: For the libraries and tools that make this project possible.

---

## Contact

For any questions or suggestions, please contact:

- **Your Name**
- **Email**: 2303732@sit.singaporetech.edu.sg
- **GitHub**: [SKAFahad](https://github.com/SKAFahad)

---

## Frequently Asked Questions (FAQ)

### 1. Does the application support other file formats besides PDF and DOCX?

Currently, the application supports PDF and DOCX files. Support for additional formats may be added in future updates.

### 2. Do I need a GPU to run this application?

A GPU is not required but can significantly speed up tasks involving NLP models, such as title generation.

### 3. Is my data secure when using this application?

Yes, all processing is done locally on your machine. No data is sent to external servers, ensuring data privacy.

---

## Future Enhancements

- **Support for Additional File Formats**: Expand compatibility to include other document types like HTML or plain text files.
- **Advanced NLP Features**: Implement more sophisticated models for improved relationship mapping and content analysis.
- **Graphical User Interface (GUI)**: Develop a user-friendly interface using tools like `tkinter` or `Streamlit`.
- **Performance Optimization**: Explore parallel processing and other techniques to improve application speed.

---

## Project Status

This project is under active development. Feedback and contributions are greatly appreciated to enhance functionality and usability.

---

## Changelog

- **v1.0.0**
  - Initial release with core features:
    - Text, image, and table extraction.
    - Relationship mapping.
    - PDF report generation with NLP-based title.
