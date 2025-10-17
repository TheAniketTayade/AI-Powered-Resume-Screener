"""
Demo script for the AI-Powered Resume Screener
This script demonstrates the key functionality without requiring a full deployment
"""
import json
import os
from gemini_analysis import analyze_resumes_with_gemini

def create_sample_resumes():
    """Create sample resume data for demonstration"""
    return [
        {
            "filename": "john_smith_resume.pdf",
            "text": """
            John Smith
            Software Engineer
            
            Experience:
            - 5 years Python development
            - Machine Learning expertise with TensorFlow and PyTorch
            - Cloud platforms (AWS, GCP)
            - Full-stack development with React and Node.js
            
            Education:
            - BS Computer Science, Stanford University
            
            Skills:
            - Python, JavaScript, React, Node.js
            - TensorFlow, PyTorch, Scikit-learn
            - Docker, Kubernetes, AWS, GCP
            - SQL, MongoDB, PostgreSQL
            """
        },
        {
            "filename": "sarah_johnson_resume.pdf",
            "text": """
            Sarah Johnson
            Data Scientist
            
            Experience:
            - 3 years data science experience
            - Strong background in statistics and machine learning
            - Experience with big data tools (Spark, Hadoop)
            - Python and R programming
            
            Education:
            - MS Data Science, MIT
            - BS Mathematics, UC Berkeley
            
            Skills:
            - Python, R, SQL
            - Machine Learning, Deep Learning
            - TensorFlow, PyTorch, Scikit-learn
            - Spark, Hadoop, Kafka
            - Tableau, PowerBI
            """
        },
        {
            "filename": "mike_chen_resume.pdf",
            "text": """
            Mike Chen
            DevOps Engineer
            
            Experience:
            - 4 years DevOps and infrastructure experience
            - Strong background in cloud platforms
            - CI/CD pipeline development
            - Container orchestration
            
            Education:
            - BS Computer Engineering, UC San Diego
            
            Skills:
            - Docker, Kubernetes, Jenkins
            - AWS, Azure, GCP
            - Terraform, Ansible
            - Python, Bash, PowerShell
            - Monitoring and logging tools
            """
        }
    ]

def create_sample_job_description():
    """Create a sample job description for demonstration"""
    return """
    Senior Software Engineer - Machine Learning
    
    We are looking for a Senior Software Engineer with expertise in machine learning and cloud platforms.
    
    Requirements:
    - 3+ years of Python development experience
    - Strong background in machine learning and data science
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Knowledge of containerization (Docker, Kubernetes)
    - Experience with ML frameworks (TensorFlow, PyTorch)
    - Strong problem-solving and communication skills
    
    Responsibilities:
    - Develop and deploy machine learning models
    - Build scalable cloud applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Contribute to technical architecture decisions
    """

def run_demo():
    """Run the demonstration"""
    print("🤖 AI-Powered Resume Screener Demo")
    print("=" * 50)
    
    # Check if Gemini API key is available
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not found in environment variables")
        print("   Please set your Gemini API key to run the full demo")
        print("   For now, showing sample data structure...")
        
        # Show sample data without API call
        resumes = create_sample_resumes()
        job_description = create_sample_job_description()
        
        print(f"\n📄 Sample Resumes ({len(resumes)} files):")
        for i, resume in enumerate(resumes, 1):
            print(f"   {i}. {resume['filename']}")
        
        print(f"\n📝 Job Description:")
        print(f"   {job_description[:100]}...")
        
        print(f"\n🔍 Sample Analysis Results:")
        sample_results = [
            {
                "name": "John Smith",
                "match_score": 85,
                "summary": "John has 5+ years of Python development experience and strong machine learning background. His experience with cloud platforms and full-stack development makes him an excellent fit for this role.",
                "missing_skills": ["Kubernetes", "Terraform"]
            },
            {
                "name": "Sarah Johnson", 
                "match_score": 78,
                "summary": "Sarah has strong data science background with 3 years experience and relevant ML skills. Her statistical background and big data experience are valuable assets.",
                "missing_skills": ["Docker", "Cloud platforms", "Full-stack development"]
            },
            {
                "name": "Mike Chen",
                "match_score": 65,
                "summary": "Mike has excellent DevOps and infrastructure experience with strong cloud platform knowledge. However, he lacks direct machine learning development experience.",
                "missing_skills": ["Machine Learning", "Data Science", "ML frameworks"]
            }
        ]
        
        for i, candidate in enumerate(sample_results, 1):
            print(f"\n   #{i} {candidate['name']} - Score: {candidate['match_score']}/100")
            print(f"   Summary: {candidate['summary']}")
            print(f"   Missing Skills: {', '.join(candidate['missing_skills'])}")
        
        return
    
    # Run full demo with Gemini API
    try:
        print("🔧 Running full demo with Gemini AI...")
        
        resumes = create_sample_resumes()
        job_description = create_sample_job_description()
        
        print(f"📄 Processing {len(resumes)} resumes...")
        print(f"📝 Job Description: {job_description[:100]}...")
        
        # Analyze with Gemini
        results = analyze_resumes_with_gemini(resumes, job_description)
        
        print("\n🔍 Analysis Results:")
        print("=" * 30)
        
        if isinstance(results, list):
            for i, candidate in enumerate(results, 1):
                print(f"\n#{i} {candidate.get('name', 'Unknown')} - Score: {candidate.get('match_score', 0)}/100")
                print(f"Summary: {candidate.get('summary', 'No summary')}")
                print(f"Missing Skills: {', '.join(candidate.get('missing_skills', []))}")
        else:
            print("Results:", results)
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("   Please check your Gemini API key and try again")

if __name__ == "__main__":
    run_demo()
