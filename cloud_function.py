"""
Cloud Function for processing uploaded resumes
This function is triggered when files are uploaded to Cloud Storage
"""
import functions_framework
from google.cloud import storage
from google.cloud import aiplatform
import json
import tempfile
import os
from text_extraction import extract_text_from_file

@functions_framework.http
def process_resume_upload(request):
    """
    Cloud Function triggered by Cloud Storage upload
    
    Args:
        request: HTTP request object
        
    Returns:
        HTTP response
    """
    try:
        # Parse the request
        request_json = request.get_json()
        
        if not request_json:
            return {"error": "No JSON payload"}, 400
        
        # Extract file information
        bucket_name = request_json.get('bucket')
        file_name = request_json.get('name')
        
        if not bucket_name or not file_name:
            return {"error": "Missing bucket or file name"}, 400
        
        # Initialize clients
        storage_client = storage.Client()
        aiplatform.init()
        
        # Download and process the file
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
            blob.download_to_filename(temp_file.name)
            
            # Extract text
            text_content = extract_text_from_file(temp_file.name)
            
            # Clean up temporary file
            os.unlink(temp_file.name)
        
        # Index the document in Vertex AI Search
        search_engine_id = index_document_to_search(
            file_name, 
            text_content,
            request_json.get('project_id')
        )
        
        return {
            "status": "success",
            "file_name": file_name,
            "text_length": len(text_content),
            "search_engine_id": search_engine_id
        }
        
    except Exception as e:
        return {"error": str(e)}, 500

def index_document_to_search(file_name: str, text_content: str, project_id: str) -> str:
    """
    Index a document to Vertex AI Search
    
    Args:
        file_name: Name of the file
        text_content: Extracted text content
        project_id: GCP Project ID
        
    Returns:
        Search engine ID
    """
    # This is a simplified implementation
    # In practice, you would use the Vertex AI Search API
    
    # Mock implementation - in reality, you would:
    # 1. Create or get a search engine
    # 2. Upload the document
    # 3. Configure search settings
    
    search_engine_id = f"resume-search-{project_id}"
    
    # Store document metadata (in practice, this would be in Vertex AI Search)
    document_data = {
        "name": file_name,
        "content": text_content,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    # In a real implementation, you would store this in Vertex AI Search
    print(f"Indexing document: {file_name}")
    print(f"Content length: {len(text_content)}")
    
    return search_engine_id
