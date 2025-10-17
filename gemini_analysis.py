"""
Gemini AI analysis for resume screening
"""
import google.generativeai as genai
from typing import List, Dict
import json

def analyze_resumes_with_gemini(resume_texts: List[Dict], job_description: str) -> List[Dict]:
    """
    Analyze resumes using Gemini AI
    
    Args:
        resume_texts: List of dictionaries with 'filename' and 'text'
        job_description: Job description text
        
    Returns:
        List of top 5 candidates with analysis
    """
    
    # Configure Gemini
    model = genai.GenerativeModel('gemini-pro')
    
    # Create the analysis prompt
    prompt = create_analysis_prompt(resume_texts, job_description)
    
    try:
        # Generate analysis
        response = model.generate_content(prompt)
        
        # Parse the response
        results = parse_gemini_response(response.text)
        
        return results
        
    except Exception as e:
        raise Exception(f"Error in Gemini analysis: {str(e)}")

def create_analysis_prompt(resume_texts: List[Dict], job_description: str) -> str:
    """
    Create the analysis prompt for Gemini
    
    Args:
        resume_texts: List of resume data
        job_description: Job description
        
    Returns:
        Formatted prompt string
    """
    
    # Prepare resume data for the prompt
    resume_data = ""
    for i, resume in enumerate(resume_texts, 1):
        resume_data += f"\n--- RESUME {i}: {resume['filename']} ---\n"
        resume_data += resume['text'][:2000] + "...\n"  # Limit text length
    
    prompt = f"""
You are an expert technical recruiter with 15+ years of experience. Your task is to analyze the provided resumes and compare them against the job description to identify the top 5 candidates.

JOB DESCRIPTION:
{job_description}

RESUMES TO ANALYZE:
{resume_data}

INSTRUCTIONS:
1. Carefully read each resume and the job description
2. Identify key skills, experience, and qualifications mentioned in the job description
3. For each resume, assess how well the candidate matches the job requirements
4. Consider both technical skills and soft skills
5. Look for relevant experience, education, and achievements
6. Identify any missing skills or qualifications

OUTPUT FORMAT:
Return a JSON array with exactly 5 candidates (or fewer if less than 5 resumes provided). Each candidate object should have:
- "name": Candidate's name (extract from resume)
- "match_score": Integer from 0-100 representing match quality
- "summary": 2-sentence summary explaining why they are a good fit
- "missing_skills": Array of key skills they are missing (be specific)

EXAMPLE OUTPUT:
[
  {{
    "name": "John Smith",
    "match_score": 85,
    "summary": "John has 5+ years of Python development experience and strong machine learning background. His experience with cloud platforms and data analysis makes him an excellent fit for this role.",
    "missing_skills": ["Docker", "Kubernetes", "React"]
  }}
]

IMPORTANT:
- Return ONLY valid JSON
- Include exactly 5 candidates (or fewer if less resumes)
- Be specific about missing skills
- Focus on the most relevant candidates
- Consider both technical and soft skills
"""
    
    return prompt

def parse_gemini_response(response_text: str) -> List[Dict]:
    """
    Parse Gemini's response and extract the JSON
    
    Args:
        response_text: Raw response from Gemini
        
    Returns:
        Parsed list of candidates
    """
    try:
        # Try to find JSON in the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            # If no JSON found, try to parse the entire response
            return json.loads(response_text)
            
    except json.JSONDecodeError as e:
        # If JSON parsing fails, create a fallback response
        return create_fallback_response(response_text)

def create_fallback_response(response_text: str) -> List[Dict]:
    """
    Create a fallback response when JSON parsing fails
    
    Args:
        response_text: Raw response from Gemini
        
    Returns:
        Fallback candidate list
    """
    return [
        {
            "name": "Analysis Error",
            "match_score": 0,
            "summary": "Unable to parse AI response. Please try again.",
            "missing_skills": ["Response parsing failed"]
        }
    ]

def validate_candidate_data(candidates: List[Dict]) -> List[Dict]:
    """
    Validate and clean candidate data
    
    Args:
        candidates: List of candidate dictionaries
        
    Returns:
        Validated and cleaned candidate data
    """
    validated = []
    
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
            
        validated_candidate = {
            "name": candidate.get("name", "Unknown"),
            "match_score": max(0, min(100, int(candidate.get("match_score", 0)))),
            "summary": candidate.get("summary", "No summary available"),
            "missing_skills": candidate.get("missing_skills", [])
        }
        
        # Ensure missing_skills is a list
        if not isinstance(validated_candidate["missing_skills"], list):
            validated_candidate["missing_skills"] = []
        
        validated.append(validated_candidate)
    
    return validated
