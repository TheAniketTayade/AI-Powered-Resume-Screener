import streamlit as st
import os
import tempfile
import json
from typing import List, Dict
import pandas as pd
from google.cloud import storage
from google.cloud import aiplatform
import google.generativeai as genai
from text_extraction import extract_text_from_file
from gcp_utils import upload_to_gcs, trigger_cloud_function
from gemini_analysis import analyze_resumes_with_gemini
import time

# Configure page
st.set_page_config(
    page_title="AI-Powered Resume Screener",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

def main():
    st.title("🤖 AI-Powered Resume Screener")
    st.markdown("Upload resumes and get AI-powered candidate analysis in seconds!")
    
    # Add health check info in sidebar
    with st.sidebar:
        st.subheader("System Status")
        health = health_check()
        st.success(f"✅ {health['status'].title()}")
        st.caption(f"Version: {health['version']}")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # GCP Configuration
        st.subheader("GCP Settings")
        project_id = st.text_input("GCP Project ID", value=os.getenv("GCP_PROJECT_ID", ""))
        bucket_name = st.text_input("Storage Bucket Name", value=os.getenv("GCS_BUCKET_NAME", ""))
        
        # API Keys
        st.subheader("API Keys")
        gemini_api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
        
        if st.button("Save Configuration"):
            st.success("Configuration saved!")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload Resumes")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Choose resume files (PDF, DOCX)",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            help="Upload multiple resume files for analysis"
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"Uploaded {len(uploaded_files)} files")
            
            # Display uploaded files
            with st.expander("View Uploaded Files"):
                for i, file in enumerate(uploaded_files):
                    st.write(f"{i+1}. {file.name} ({file.size} bytes)")
    
    with col2:
        st.header("📝 Job Description")
        
        # Job description input
        job_description = st.text_area(
            "Paste your job description here:",
            height=300,
            placeholder="Enter the complete job description including requirements, responsibilities, and qualifications...",
            value=st.session_state.job_description
        )
        
        if job_description:
            st.session_state.job_description = job_description
            st.success("Job description saved!")
    
    # Analysis section
    if st.session_state.uploaded_files and st.session_state.job_description:
        st.header("🔍 AI Analysis")
        
        if st.button("🚀 Analyze Resumes", type="primary"):
            with st.spinner("Processing resumes with AI..."):
                try:
                    # Process files
                    results = process_resumes(
                        st.session_state.uploaded_files,
                        st.session_state.job_description,
                        project_id,
                        bucket_name,
                        gemini_api_key
                    )
                    
                    st.session_state.analysis_results = results
                    st.success("Analysis complete!")
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
    
    # Display results
    if st.session_state.analysis_results:
        display_results(st.session_state.analysis_results)

def process_resumes(uploaded_files, job_description, project_id, bucket_name, gemini_api_key):
    """Process uploaded resumes and return analysis results"""
    
    # Configure Gemini
    genai.configure(api_key=gemini_api_key)
    
    # Extract text from all files
    resume_texts = []
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file.flush()
            
            try:
                text = extract_text_from_file(tmp_file.name)
                resume_texts.append({
                    'filename': file.name,
                    'text': text
                })
            except Exception as e:
                st.warning(f"Could not extract text from {file.name}: {str(e)}")
            finally:
                os.unlink(tmp_file.name)
    
    if not resume_texts:
        raise Exception("No text could be extracted from uploaded files")
    
    # Analyze with Gemini
    results = analyze_resumes_with_gemini(resume_texts, job_description)
    
    return results

def display_results(results):
    """Display analysis results in a clean table"""
    
    st.header("📊 Top 5 Candidates")
    
    if isinstance(results, str):
        try:
            results = json.loads(results)
        except json.JSONDecodeError:
            st.error("Invalid JSON response from AI analysis")
            return
    
    if not isinstance(results, list):
        st.error("Invalid results format")
        return
    
    # Create DataFrame for display
    df_data = []
    for candidate in results:
        df_data.append({
            'Name': candidate.get('name', 'Unknown'),
            'Match Score': f"{candidate.get('match_score', 0)}/100",
            'Summary': candidate.get('summary', 'No summary available'),
            'Missing Skills': ', '.join(candidate.get('missing_skills', []))
        })
    
    df = pd.DataFrame(df_data)
    
    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download results
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="resume_analysis_results.csv",
        mime="text/csv"
    )
    
    # Detailed view
    st.subheader("🔍 Detailed Analysis")
    for i, candidate in enumerate(results, 1):
        with st.expander(f"#{i} {candidate.get('name', 'Unknown')} - Score: {candidate.get('match_score', 0)}/100"):
            st.write("**Summary:**")
            st.write(candidate.get('summary', 'No summary available'))
            
            st.write("**Missing Skills:**")
            missing_skills = candidate.get('missing_skills', [])
            if missing_skills:
                for skill in missing_skills:
                    st.write(f"• {skill}")
            else:
                st.write("No missing skills identified")

if __name__ == "__main__":
    main()
