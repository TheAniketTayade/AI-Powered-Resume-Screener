@echo off
REM AI-Powered Resume Screener Deployment Script for Windows
REM This script deploys the application to Google Cloud Run

echo 🚀 Deploying AI-Powered Resume Screener to Google Cloud Run
echo ============================================================

REM Check if gcloud is installed
gcloud version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ gcloud CLI is not installed. Please install it first.
    exit /b 1
)

REM Check if user is authenticated
gcloud auth list --filter=status:ACTIVE --format="value(account)" | findstr . >nul
if %errorlevel% neq 0 (
    echo ❌ Not authenticated with gcloud. Please run 'gcloud auth login' first.
    exit /b 1
)

REM Get project ID
for /f "tokens=*" %%i in ('gcloud config get-value project') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo ❌ No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID' first.
    exit /b 1
)

echo 📋 Project ID: %PROJECT_ID%

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudfunctions.googleapis.com

REM Create storage bucket if it doesn't exist
set BUCKET_NAME=resume-screener-%RANDOM%
echo 🪣 Creating storage bucket: %BUCKET_NAME%
gsutil mb gs://%BUCKET_NAME% 2>nul || echo Bucket might already exist

REM Build and deploy
echo 🏗️ Building and deploying application...
gcloud builds submit --config cloudbuild.yaml

REM Get the service URL
for /f "tokens=*" %%i in ('gcloud run services describe resume-screener --region=us-central1 --format="value(status.url)"') do set SERVICE_URL=%%i

echo ✅ Deployment completed!
echo 🌐 Service URL: %SERVICE_URL%
echo.
echo 📝 Next steps:
echo 1. Set environment variables in Cloud Run console
echo 2. Configure your Gemini API key
echo 3. Test the application with sample resumes
echo.
echo 🔧 To set environment variables:
echo gcloud run services update resume-screener ^
echo   --set-env-vars="GCP_PROJECT_ID=%PROJECT_ID%,GCS_BUCKET_NAME=%BUCKET_NAME%,GEMINI_API_KEY=your-api-key"

pause
