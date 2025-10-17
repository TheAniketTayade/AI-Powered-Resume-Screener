#!/bin/bash

# AI-Powered Resume Screener Deployment Script
# This script deploys the application to Google Cloud Run

set -e

echo "🚀 Deploying AI-Powered Resume Screener to Google Cloud Run"
echo "============================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login' first."
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID' first."
    exit 1
fi

echo "📋 Project ID: $PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudfunctions.googleapis.com

# Create storage bucket if it doesn't exist
BUCKET_NAME="resume-screener-$(date +%s)"
echo "🪣 Creating storage bucket: $BUCKET_NAME"
gsutil mb gs://$BUCKET_NAME || echo "Bucket might already exist"

# Build and deploy
echo "🏗️ Building and deploying application..."
gcloud builds submit --config cloudbuild.yaml

# Get the service URL
SERVICE_URL=$(gcloud run services describe resume-screener --region=us-central1 --format="value(status.url)")

echo "✅ Deployment completed!"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "📝 Next steps:"
echo "1. Set environment variables in Cloud Run console"
echo "2. Configure your Gemini API key"
echo "3. Test the application with sample resumes"
echo ""
echo "🔧 To set environment variables:"
echo "gcloud run services update resume-screener \\"
echo "  --set-env-vars=\"GCP_PROJECT_ID=$PROJECT_ID,GCS_BUCKET_NAME=$BUCKET_NAME,GEMINI_API_KEY=your-api-key\""
