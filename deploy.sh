#!/bin/bash

echo "Pulling latest image..."
docker pull ghcr.io/feliciasharon/mental-health-mlops-nlp:latest

echo "Updating Kubernetes deployment..."
kubectl set image deployment/mental-health-app \
app=ghcr.io/feliciasharon/mental-health-mlops-nlp:latest

echo "Waiting for rollout..."
kubectl rollout status deployment/mental-health-app

echo "Done 🚀"
