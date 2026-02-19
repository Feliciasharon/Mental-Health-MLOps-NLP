#!/bin/bash

echo "Pulling latest image..."
docker pull ghcr.io/feliciasharon/mental-health-mlops-nlp:latest

echo "Updating Kubernetes deployment..."
kubectl set image deployment/mental-health-app \
app=ghcr.io/feliciasharon/mental-health-mlops-nlp:latest

kubectl apply -f k8s/deployment.yaml 

echo "Restarting pods.."
kubectl rollout restart deployment mental-health-app   

echo "Waiting for rollout..."
kubectl rollout status deployment/mental-health-app

echo "Done 🚀"

echo "Viewing status of new deployments.."
kubectl get pods
