"""
Text extraction utilities for PDF and DOCX files
"""
import os
import PyPDF2
from docx import Document
from typing import Optional

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a file (PDF or DOCX)
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text content
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    text = ""
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
                
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
    
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file_path: Path to DOCX file
        
    Returns:
        Extracted text content
    """
    text = ""
    
    try:
        doc = Document(file_path)
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")
    
    return text.strip()

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove common PDF artifacts
    text = text.replace('\x00', '')  # Remove null characters
    text = text.replace('\ufeff', '')  # Remove BOM
    
    return text.strip()
