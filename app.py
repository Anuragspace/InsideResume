# FLASK APP - Run the app using flask --app app.py run
import os, sys
from flask import Flask, request, render_template
from pypdf import PdfReader 
import json
from resumeparser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def ats():
    try:
        doc = request.files['pdf_doc']
        doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
        doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
        data = _read_file_from_path(doc_path)
        
        if not data.strip():
            error_data = {
                "error": "Could not extract text from PDF",
                "full_name": "PDF text extraction failed",
                "email_id": "PDF text extraction failed",
                "github_portfolio": "PDF text extraction failed",
                "linkedin_id": "PDF text extraction failed", 
                "employment_details": ["Could not read PDF content"],
                "technical_skills": ["Could not read PDF content"],
                "soft_skills": ["Could not read PDF content"]
            }
            return render_template('index.html', data=error_data)
        
        parsed_data = ats_extractor(data)
        
        try:
            json_data = json.loads(parsed_data)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {parsed_data}")
            error_data = {
                "error": f"JSON parsing failed: {str(e)}",
                "raw_response": parsed_data[:500] + "..." if len(parsed_data) > 500 else parsed_data,
                "full_name": "JSON parsing failed",
                "email_id": "JSON parsing failed",
                "github_portfolio": "JSON parsing failed",
                "linkedin_id": "JSON parsing failed",
                "employment_details": ["JSON parsing failed"],
                "technical_skills": ["JSON parsing failed"], 
                "soft_skills": ["JSON parsing failed"]
            }
            return render_template('index.html', data=error_data)

        return render_template('index.html', data=json_data)
        
    except Exception as e:
        print(f"General error in /process route: {str(e)}")
        error_data = {
            "error": str(e),
            "full_name": "System error",
            "email_id": "System error",
            "github_portfolio": "System error", 
            "linkedin_id": "System error",
            "employment_details": ["System error occurred"],
            "technical_skills": ["System error occurred"],
            "soft_skills": ["System error occurred"]
        }
        return render_template('index.html', data=error_data)
 
def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no] 
        data += page.extract_text()

    return data 


if __name__ == "__main__":
    app.run(port=8000, debug=True)

