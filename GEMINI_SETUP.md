# Google Gemini Integration Setup

This project has been updated to use Google Gemini instead of OpenAI for resume parsing.

## Changes Made:

1. **Dependencies Updated**: 
   - Replaced `openai==1.16.2` with `google-generativeai==0.8.3`
   - Added `PyYAML==6.0.1` for better YAML handling

2. **Configuration Updated**:
   - `config.yaml` now uses `GEMINI_API_KEY`

3. **Code Updated**:
   - `resumeparser.py` now uses Google Gemini API (`gemini-1.5-flash` model)
   - Simplified prompt handling for better compatibility

## Setup Instructions:

### 1. Get Gemini API Key
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a new API key
- Copy the API key

### 2. Update Configuration
- Open `config.yaml`
- Replace `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python app.py
```

## Benefits of Using Gemini:

- **Cost-effective**: Gemini often provides better pricing compared to OpenAI
- **Performance**: Fast response times
- **Free tier**: Google provides generous free usage limits
- **Latest model**: Uses the latest Gemini 1.5 Flash model

## Model Details:
- **Model**: `gemini-1.5-flash`
- **Provider**: Google AI
- **Features**: Multimodal capabilities, fast inference, cost-effective

The functionality remains the same - upload your PDF resume and get parsed information in JSON format!
