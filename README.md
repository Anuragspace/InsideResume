# 🚀 Intelligent Resume Parser App (Gen AI + Flask)

## 📝 Overview

InsideResume is an AI-powered resume parsing application built with Flask. It enables job seekers to test the ATS (Applicant Tracking System) friendliness of their resumes by extracting and analyzing essential details. The app parses PDF resumes and provides a comprehensive JSON summary, helping users optimize their resumes for modern recruitment systems.

[![🔴 Live Demo](https://img.shields.io/badge/Try%20Live%20Demo-Insideresume.onrender.com-green?style=for-the-badge&logo=google-chrome)](https://insideresume.onrender.com/)

## ✨ Features

- 🤖 **AI Resume Parsing:** Extracts personal details, employment history, education, skills, and more using advanced NLP and LLMs (Gemini AI or OpenAI).
- 🎯 **ATS Compatibility Score:** Evaluates how well a resume is likely to perform in automated recruitment systems.
- 🛠️ **Skill Analysis:** Breaks down technical, soft, and domain skills from the document.
- 📝 **Professional Summary & Suggestions:** Provides a parsed professional summary and areas of improvement.
- 💼 **Job Role Recommendations:** Suggests relevant job roles based on resume content.
- 🧑‍💻 **Project & Research Extraction:** Identifies and summarizes projects and research work.
- 🌈 **Interactive Web UI:** Modern, responsive interface for resume upload and results visualization.
- 🔄 **Support for Google Gemini & OpenAI:** Easily switch between LLM providers (see [GEMINI_SETUP.md](GEMINI_SETUP.md) for Gemini integration).

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS (Tailwind used in templates)
- **AI/NLP:** Google Gemini API (default), OpenAI API (legacy/support), spaCy, NLTK, PyYAML
- **Parsing:** pdfminer.six, docx2txt
- **Other:** YAML for configuration, JSON for output

## 📁 File Structure

- `app.py` – Flask web server (main entry point)
- `resumeparser.py` – Core resume parsing logic, LLM integration, NLP extraction
- `requirements.txt` – Python dependencies
- `templates/index.html` – Main web UI (upload, results, scoring, suggestions)
- `config.yaml` – Configuration file (API keys, provider selection)
- `GEMINI_SETUP.md` – Instructions for switching to Google Gemini API
- *(other supporting files as needed)*

## 👀 Sneak Peek

![image](https://github.com/pik1989/Resume-Parser-OpenAI/assets/34673684/5d206207-1b25-4dbe-8e11-add701b632e7)

## ⚡️ Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Anuragspace/InsideResume.git
    cd InsideResume
    ```
2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Setup AI Provider:**
   - For Google Gemini, follow [GEMINI_SETUP.md](GEMINI_SETUP.md) and add your `GEMINI_API_KEY` to `config.yaml`.
   - For OpenAI, add your API key to `config.yaml`.

## 🧑‍💻 Usage

1. **Start the application:**
    ```sh
    python app.py
    ```
2. **Open your browser:**  
   Go to [https://localhost:8000](https://localhost:8000)
3. **Upload your resume (.pdf):**
   - The app parses, analyzes, and displays ATS score, skills, summary, job roles, and suggestions.

Or try it instantly:  
[![🟢 Go To Live App](https://img.shields.io/badge/Open%20InsideResume%20Online-Insideresume.onrender.com-blue?style=for-the-badge&logo=google-chrome)](https://insideresume.onrender.com/)

## 🏃 Running All

- ⚙️ Ensure your API key is set in `config.yaml`.
- ▶️ Run `python app.py` and access via browser.
- 🗂️ For Gemini setup/advanced options, see [GEMINI_SETUP.md](GEMINI_SETUP.md).

---

## 💡 Modern Recruitment Technology

InsideResume leverages the latest in AI and NLP to help job seekers optimize their resumes for ATS and recruiter visibility, bridging the gap between applicants and modern hiring technology.

## 🤝 Contributing

Pull requests and suggestions are welcome! Please open an issue for any bugs or feature requests.

## ⚖️ License

This project is released under the MIT License.
