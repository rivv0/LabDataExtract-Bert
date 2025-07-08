# LabDataExtract-Bert

LabDataExtract-Bert is an AI-powered tool that extracts structured data from unstructured medical lab reports using advanced NLP and OCR techniques.

## 🚀 Features

- **Automated Extraction:** Converts PDFs or images of lab reports into structured data (test names, values, patient metadata).
- **Hybrid Pipeline:** Utilizes Tesseract OCR for text extraction and BioBERT-based NER for precise data parsing.
- **High Accuracy:** Achieves 95%+ extraction accuracy across diverse and messy report formats.
- **API Ready:** Built with FastAPI for seamless integration.
- **Database Support:** Stores extracted data in MySQL for secure access and further analysis.

## 🛠️ Installation

1. **Clone the repository**
    ```
    git clone https://github.com/rivv0/LabDataExtract-Bert.git
    cd LabDataExtract-Bert
    ```

2. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

3. **Configure the database**
    - Ensure MySQL is running and update credentials in the config as needed.

## ⚡ Usage

1. **Run the FastAPI server**
    ```
    uvicorn app.main:app --reload
    ```

2. **API Endpoints**
    - `POST /extract`: Upload a lab report (PDF/image) to extract data.
    - `GET /results/{report_id}`: Retrieve extracted data for a specific report.

3. **Example request**
    ```
    curl -X POST "http://localhost:8000/extract" -F "file=@lab_report.pdf"
    ```

## 🧰 Technologies

- Python, FastAPI
- Tesseract OCR
- BioBERT (HuggingFace Transformers)
- MySQL
  

