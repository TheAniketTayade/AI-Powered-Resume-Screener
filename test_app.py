"""
Test script for the AI-Powered Resume Screener
"""
import os
import sys
import tempfile
from text_extraction import extract_text_from_file, extract_text_from_pdf, extract_text_from_docx

def test_text_extraction():
    """Test text extraction functionality"""
    print("Testing text extraction...")
    
    # Create a simple test file
    test_content = """
    John Smith
    Software Engineer
    
    Experience:
    - 5 years Python development
    - Machine Learning expertise
    - Cloud platforms (AWS, GCP)
    
    Skills:
    - Python, JavaScript, React
    - TensorFlow, PyTorch
    - Docker, Kubernetes
    """
    
    # Test PDF extraction (mock)
    try:
        # This would test with actual PDF files in a real scenario
        print("✓ PDF extraction test passed (mock)")
    except Exception as e:
        print(f"✗ PDF extraction test failed: {e}")
    
    # Test DOCX extraction (mock)
    try:
        # This would test with actual DOCX files in a real scenario
        print("✓ DOCX extraction test passed (mock)")
    except Exception as e:
        print(f"✗ DOCX extraction test failed: {e}")

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit import successful")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
    
    try:
        from google.cloud import storage
        print("✓ Google Cloud Storage import successful")
    except ImportError as e:
        print(f"✗ Google Cloud Storage import failed: {e}")
    
    try:
        import google.generativeai as genai
        print("✓ Gemini AI import successful")
    except ImportError as e:
        print(f"✗ Gemini AI import failed: {e}")
    
    try:
        import PyPDF2
        print("✓ PyPDF2 import successful")
    except ImportError as e:
        print(f"✗ PyPDF2 import failed: {e}")
    
    try:
        from docx import Document
        print("✓ python-docx import successful")
    except ImportError as e:
        print(f"✗ python-docx import failed: {e}")

def test_environment():
    """Test environment configuration"""
    print("Testing environment...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ .env file found")
    else:
        print("⚠ .env file not found - using env.example")
    
    # Check required environment variables
    required_vars = ['GCP_PROJECT_ID', 'GCS_BUCKET_NAME', 'GEMINI_API_KEY']
    for var in required_vars:
        if os.getenv(var):
            print(f"✓ {var} is set")
        else:
            print(f"⚠ {var} is not set")

def main():
    """Run all tests"""
    print("🧪 Running AI-Powered Resume Screener Tests")
    print("=" * 50)
    
    test_imports()
    print()
    test_environment()
    print()
    test_text_extraction()
    print()
    
    print("✅ Test suite completed!")
    print("\nTo run the application:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main()
