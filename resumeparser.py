from flask import Flask, render_template, request
import json
import httpx
import yaml
from PyPDF2 import PdfReader

app = Flask(__name__)

# Load API key from config
CONFIG_PATH = "config.yaml"

def load_api_key():
    with open(CONFIG_PATH) as file:
        data = yaml.safe_load(file)
        return data.get('OPENROUTER_API_KEY')

api_key = load_api_key()

def ats_extractor(resume_data):
    """Extracts ATS data from resume using OpenRouter API"""
    try:
        prompt = '''You are an ATS professional for parsing resumes. Extract:
        1. full name
        2. Gmail
        3. github
        4. linkedin, other profiles
        5. employment details
        6. technical skills
        7. soft skills,
        8. recommended job roles
        9. pros/cons
        10. suggestions,
        11. ats rating out of 100. 
        
        Give the extracted information in given order in json format only'''

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": resume_data}
        ]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4.1",
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": 1500
        }

        with httpx.Client() as client:
            response = client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        return json.dumps({"error": f"API error: {response.status_code}"})

    except Exception as e:
        return json.dumps({"error": str(e)})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'pdf_doc' not in request.files:
        return render_template('index.html', error="No file uploaded")
    
    file = request.files['pdf_doc']
    if file.filename == '':
        return render_template('index.html', error="No file selected")

    try:
        # Extract text from PDF
        reader = PdfReader(file)
        resume_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        if not resume_text:
            return render_template('index.html', error="Could not extract text from PDF")

        # Parse resume
        parsed_data = ats_extractor(resume_text)
        data = json.loads(parsed_data)
        
        if 'error' in data:
            return render_template('index.html', error=data['error'])
            
        return render_template('index.html', data=data)

    except json.JSONDecodeError:
        return render_template('index.html', error="Invalid response from parser")
    except Exception as e:
        return render_template('index.html', error=f"Processing error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)