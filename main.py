import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai
import os
import openpyxl
from pathlib import Path
import io

# Set up Google API Key
GOOGLE_API_KEY = os.getenv('AIzaSyC15hBMiMRDoF42JRuiHrCfrmC2VM6IKF8')  # Store your Google API Key securely
genai.configure(api_key='AIzaSyC15hBMiMRDoF42JRuiHrCfrmC2VM6IKF8')

# Model Configuration
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Safety Settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize Gemini Model
model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=MODEL_CONFIG,
                              safety_settings=safety_settings)


# Function to convert the single-page PDF to an image
def pdf_to_image(pdf_path):
    try:
        doc = fitz.open(pdf_path)  # Open the PDF using PyMuPDF
        page = doc[0]  # Access the first page
        pix = page.get_pixmap()  # Get the image representation of the page
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    except Exception as e:
        raise ValueError(f"Error converting PDF to image: {e}")


# Function to generate Gemini output
def gemini_output(image, system_prompt, user_prompt):
    try:
        # Convert the image to a byte array for the API
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)  # Go to the start of the byte array

        # Send image and prompts to Gemini for processing
        input_prompt = [system_prompt, {"mime_type": "image/jpeg", "data": img_byte_arr.getvalue()}, user_prompt]
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        raise ValueError(f"Error generating output from Gemini: {e}")


# Function to save data and use the Text to Columns method in Excel
def save_data_to_excel_using_text_to_columns(delimited_data, delimiter, file_path):
    try:
        # Create a new workbook and select the active worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Split delimited data into rows
        rows = delimited_data.strip().split("\n")  # Split into rows by line break

        # Write the data to Excel row by row
        for row_idx, row_data in enumerate(rows, start=1):
            row_values = row_data.split(delimiter)

            # Write the delimited data to the Excel sheet
            for col_idx, value in enumerate(row_values, start=1):
                sheet.cell(row=row_idx, column=col_idx, value=value)

        # Save the workbook to the given file path
        workbook.save(file_path)

        return f"File saved successfully at {file_path}"

    except Exception as e:
        raise ValueError(f"Error saving to Excel: {e}")


# Updated Streamlit UI to handle multiple rows in delimited data
def app():
    st.title("Invoice Data Extractor")

    # Ensure the 'temp' directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # File Upload for PDF
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded PDF temporarily
        pdf_path = os.path.join("temp", uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            # Convert PDF to image
            img = pdf_to_image(pdf_path)

            # Display the image in the Streamlit app
            st.image(img, caption="Converted PDF Page", use_column_width=True)

            # System prompt for receipt processing
            system_prompt = """
            You are a specialist in comprehending receipts.
            Input images in the form of receipts will be provided to you,
            and your task is to respond to questions based on the content of the input image.
            """

            # User Prompt for balance extraction
            user_prompt = "What is the balance amount in the image?"
            balance_output = gemini_output(img, system_prompt, user_prompt)
            st.write(f"Balance Amount: {balance_output}")

            # Convert Invoice data into delimited format
            user_prompt_format = """Converts Invoice data into delimited format.You can split it at each comma:
            total_amount:,
            base_amount:,
            tax_amount:,
            recipient_name:,
            sender_name:,
            invoice_date:,
            invoice_number:
            REPLY ONLY WITH THE DATA!"""

            delimited_data = gemini_output(img, system_prompt, user_prompt_format)
            st.write("Delimited Invoice Data:")
            st.text(delimited_data)

            # Option to download the Excel file
            delimiter = ","  # Assuming CSV-style delimiter
            if st.button("Save to Excel"):
                output_path = os.path.join("temp", f"{uploaded_file.name}_invoice_table.xlsx")
                result_message = save_data_to_excel_using_text_to_columns(delimited_data, delimiter, output_path)
                st.success(result_message)
                st.download_button("Download Excel", data=open(output_path, "rb").read(),
                                   file_name=f"{uploaded_file.name}_invoice_table.xlsx")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if name == "main":
    app()