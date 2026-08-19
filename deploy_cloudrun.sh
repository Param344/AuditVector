#!/usr/bin/env bash
# Deploy AuditVector to Google Cloud Run

set -e

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="auditvector"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME:latest"

if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: GCP_PROJECT_ID is not set and could not be detected from gcloud config."
    echo "Usage: GCP_PROJECT_ID=your-project-id ./deploy_cloudrun.sh"
    exit 1
fi

echo "============================================================"
echo " DEPLOYING AUDITVECTOR TO GOOGLE CLOUD RUN"
echo " Project: $PROJECT_ID | Region: $REGION"
echo "============================================================"

# 1. Build and push image
echo "[1/2] Building container image with Google Cloud Build..."
gcloud builds submit --tag "$IMAGE_NAME" .

# 2. Deploy to Cloud Run
echo "[2/2] Deploying to Cloud Run service '$SERVICE_NAME'..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE_NAME" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars "GEMINI_MODEL=gemini-3.5-flash"

echo "============================================================"
echo " ✅ AUDITVECTOR DEPLOYMENT COMPLETE"
gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format='value(status.url)'
