# import libraries

import google.generativeai as genai
import yaml
import json
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

def ats_extractor(resume_data):

    prompt = '''
    You are an AI resume parser designed to extract comprehensive and detailed information from resumes. Extract ALL available information in its original detailed form, preserving descriptions, achievements, and context.
    
    Extract the following information from the resume:
    1. Full name
    2. Email address  
    3. Phone number
    4. LinkedIn profile URL
    5. GitHub profile URL
    6. Location/Address
    7. Professional summary/objective (full text)
    8. Complete employment history with full descriptions
    9. Complete education details 
    10. All projects with full descriptions and technologies used
    11. All technical skills (categorized if possible)
    12. All soft skills and certifications
    13. Languages spoken
    14. Awards and achievements
    15. Publications and research (if any)
    16. ATS compatibility score (0-100)
    17. Detailed areas of improvement analysis
    18. Suggested job roles based on profile
    
    IMPORTANT: Return ONLY a valid JSON object with no additional text, markdown formatting, or explanations. The response should start with { and end with }. Do not use ```json or ``` markdown formatting.
    
    Preserve ALL original descriptions, bullet points, and detailed information. Do not summarize - extract the complete raw data.
    
    Use this exact JSON structure (replace ALL example values with actual extracted data):
    {
        "full_name": "[Extract actual full name from resume]",
        "email_id": "[Extract actual email address]",
        "phone_number": "[Extract actual phone number]",
        "linkedin_id": "[Extract actual LinkedIn URL]",
        "github_portfolio": "[Extract actual GitHub URL]",
        "location": "[Extract actual location/address]",
        "professional_summary": "[Extract complete professional summary or objective section]",
        "employment_details": [
            {
                "company": "[Actual company name]",
                "position": "[Actual job title]",
                "duration": "[Actual employment duration]",
                "location": "[Actual job location]",
                "responsibilities": [
                    "[Extract each responsibility exactly as written]",
                    "[Include all bullet points and descriptions]"
                ],
                "achievements": [
                    "[Extract quantified achievements with metrics]",
                    "[Include all accomplishments mentioned]"
                ]
            }
        ],
        "education": [
            {
                "degree": "[Actual degree name]",
                "institution": "[Actual university/college name]",
                "duration": "[Actual study period]",
                "gpa": "[Actual GPA if mentioned]",
                "relevant_coursework": ["[List actual courses if mentioned]"]
            }
        ],
        "projects_and_research": [
            {
                "name": "[Actual project name]",
                "description": "[Complete project description as written]",
                "technologies": ["[List all technologies used]"],
                "duration": "[Project duration if mentioned]",
                "github_link": "[Actual GitHub link if provided]",
                "live_demo": "[Actual demo link if provided]"
            }
        ],
        "technical_skills": {
            "programming_languages": ["[Extract actual programming languages]"],
            "frameworks": ["[Extract actual frameworks and libraries]"],
            "databases": ["[Extract actual database technologies]"],
            "tools": ["[Extract actual tools and software]"],
            "other": ["[Extract other technical skills]"]
        },
        "soft_skills": ["[Extract actual soft skills mentioned]"],
        "certifications": ["[Extract actual certifications with full names]"],
        "languages": ["[Extract languages with proficiency levels]"],
        "awards_achievements": ["[Extract actual awards and recognitions]"],
        "publications": ["[Extract actual publications or research papers]"],
        "ats_score": [Calculate numerical score 0-100 based on resume quality],
        "areas_of_improvement": {
            "pros": [
                "[Analyze actual strengths based on resume content]",
                "[Identify genuine positive aspects]"
            ],
            "cons": [
                "[Identify actual areas for improvement]",
                "[Provide specific suggestions based on resume gaps]"
            ]
        },
        "preferred_job_roles": [
            "[Suggest roles based on ACTUAL skills and experience]",
            "[Match roles to candidate's specific background]"
        ]
    }
    '''

    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Try the latest models in order of preference
        model_names = [
            'gemini-2.5-flash',      # Latest experimental
            'gemini-1.5-flash-002',      # Latest stable 1.5
            'gemini-1.5-flash',          # Stable fallback
            'gemini-1.5-pro'             # Pro fallback
        ]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"Using model: {model_name}")
                break
            except Exception as e:
                print(f"Model {model_name} not available: {str(e)}")
                continue
                
        if not model:
            # Final fallback
            model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Combine prompt with resume data
        full_prompt = f"{prompt}\n\nResume Content:\n{resume_data}"
        
        # Generate response using the latest API
        response = model.generate_content(full_prompt)
        
        if not response or not response.text:
            raise Exception("No response from Gemini API")
            
        raw_response = response.text.strip()
        print(f"Raw Gemini response: {raw_response[:500]}...")  # Debug output
        
        # Clean the response - remove markdown code blocks if present
        cleaned_response = raw_response
        if raw_response.startswith('```json'):
            cleaned_response = raw_response[7:]  # Remove ```json
        elif raw_response.startswith('```'):
            cleaned_response = raw_response[3:]   # Remove ```
            
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # Remove ending ```
            
        cleaned_response = cleaned_response.strip()
        
        # Try to extract JSON if it's embedded in other text
        json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
        if json_match:
            cleaned_response = json_match.group(0)
        
        print(f"Cleaned response: {cleaned_response[:300]}...")  # Debug output
        
        # Validate JSON
        try:
            parsed_json = json.loads(cleaned_response)
            print("JSON parsing successful!")  # Debug output
            return cleaned_response
        except json.JSONDecodeError as json_err:
            print(f"JSON parsing failed: {json_err}")
            print(f"Trying to fix common JSON issues...")
            
            # Try to fix common JSON issues
            try:
                # Fix trailing commas
                fixed_response = re.sub(r',\s*}', '}', cleaned_response)
                fixed_response = re.sub(r',\s*]', ']', fixed_response)
                
                # Try parsing the fixed version
                parsed_json = json.loads(fixed_response)
                print("JSON parsing successful after fixing!")
                return fixed_response
            except json.JSONDecodeError as final_err:
                print(f"Final JSON parsing failed: {final_err}")
                # Continue to fallback response
            # If still not valid JSON, create a fallback response
            fallback_json = {
                "full_name": "Could not extract",
                "email_id": "Could not extract", 
                "phone_number": "Could not extract",
                "linkedin_id": "Could not extract",
                "github_portfolio": "Could not extract",
                "location": "Could not extract",
                "professional_summary": "Could not extract",
                "employment_details": [{"error": "Could not extract employment information"}],
                "education": [{"error": "Could not extract education information"}],
                "projects_and_research": [{"error": "Could not extract project information"}],
                "technical_skills": {"error": "Could not extract technical skills"},
                "soft_skills": ["Could not extract"],
                "certifications": ["Could not extract"],
                "languages": ["Could not extract"],
                "awards_achievements": ["Could not extract"],
                "publications": ["Could not extract"],
                "ats_score": 0,
                "areas_of_improvement": {
                    "pros": ["Could not analyze"],
                    "cons": ["Could not analyze"]
                },
                "preferred_job_roles": ["Could not determine"],
                "raw_response": raw_response[:500] + "..." if len(raw_response) > 500 else raw_response
            }
            return json.dumps(fallback_json, indent=2)
            
    except Exception as e:
        print(f"Error in ats_extractor: {str(e)}")
        # Return error information as JSON
        error_json = {
            "error": str(e),
            "full_name": "Error occurred",
            "email_id": "Error occurred",
            "phone_number": "Error occurred",
            "linkedin_id": "Error occurred",
            "github_portfolio": "Error occurred", 
            "location": "Error occurred",
            "professional_summary": "Error occurred",
            "employment_details": [{"error": "Error occurred during parsing"}],
            "education": [{"error": "Error occurred during parsing"}],
            "projects_and_research": [{"error": "Error occurred during parsing"}],
            "technical_skills": {"error": "Error occurred during parsing"},
            "soft_skills": ["Error occurred"],
            "certifications": ["Error occurred"],
            "languages": ["Error occurred"],
            "awards_achievements": ["Error occurred"],
            "publications": ["Error occurred"],
            "ats_score": 0,
            "areas_of_improvement": {
                "pros": ["Error occurred"],
                "cons": ["Error occurred"]
            },
            "preferred_job_roles": ["Error occurred"]
        }
        return json.dumps(error_json, indent=2)