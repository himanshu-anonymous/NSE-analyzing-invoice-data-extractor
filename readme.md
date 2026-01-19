# Invoice Data Extractor 📄

An automated tool designed to extract structured financial data from PDF invoices and receipts using **Google Gemini 1.5 Flash** and **Streamlit**. This project leverages computer vision and generative AI to understand document layouts and export data directly to Excel for business automation.



##  Features
* **AI-Powered Extraction**: Uses Gemini 1.5 Flash to "comprehend" invoices rather than relying on brittle, coordinate-based OCR.
* **Automatic Image Conversion**: Utilizes `PyMuPDF` to convert PDF pages into high-resolution images for optimized AI analysis.
* **Structured Data Output**: Extracts key fields including Total Amount, Tax, Base Amount, and Vendor details.
* **Excel Export**: Automatically formats extracted text into a clean `.xlsx` spreadsheet.
* **Streamlit UI**: A clean, user-friendly web interface for uploading and downloading processed files.

---

##  Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/invoice-extractor.git](https://github.com/your-username/invoice-extractor.git)
cd invoice-extractor

# Create the environment
python -m venv .venv

# Activate it (Windows)
.\.venv\Scripts\Activate.ps1

# Activate it (Mac/Linux)
source .venv/bin/activate

3. Install Dependencies
Bash

pip install -r requirements.txt

Configuration
Get a Google Gemini API Key: Visit the Google AI Studio to generate your key.

Create a .env file: In the root directory of the project, create a file named .env and add your key:

Plaintext

GOOGLE_API_KEY=your_actual_api_key_here

Usage
Launch the web interface using Streamlit:

Bash

streamlit run app.py

Upload your invoice PDF through the browser.

Preview the document as the AI processes the first page.

Review the extracted data displayed on the screen.

Download the generated Excel report.