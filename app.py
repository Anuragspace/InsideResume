import os
import sys
import json
from flask import Flask, request, render_template
from pypdf import PdfReader
from resumeparser import ats_extractor

# Ensure current directory is in path
sys.path.insert(0, os.path.abspath(os.getcwd()))

# Upload folder for storing PDFs
UPLOAD_PATH = "__DATA__"

# Create folder if it doesn't exist
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

# Initialize Flask app
app = Flask(__name__)

# Route: Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Process uploaded PDF
@app.route('/process', methods=['POST'])
def ats():
    doc = request.files.get('pdf_doc')
    if not doc:
        return render_template('index.html', data={"error": "No file uploaded"})

    # Save uploaded file
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    doc.save(doc_path)

    # Read and parse file
    data_text = _read_file_from_path(doc_path)
    extracted_data = ats_extractor(data_text)

    try:
        parsed = json.loads(extracted_data)
    except json.JSONDecodeError:
        parsed = {"error": "Failed to process resume"}

    return render_template('index.html', data=parsed)

# Helper function: Read PDF text
def _read_file_from_path(path):
    reader = PdfReader(path)
    data = ""

    for page in reader.pages:
        data += page.extract_text() or ""

    return data

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
