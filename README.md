# 🧠 Production-Grade Transformer NLP MLOps Mental Health Platform

### An end-to-end MLOps project for mental health text classification.

## This system includes:

🧠 NLP model using Sentence Transformers + Logistic Regression

🚀 FastAPI inference API

💾 PostgreSQL for prediction logging

🔁 Airflow weekly retraining

📦 Docker containerization

☸️ Kubernetes deployment

📊 Prometheus + Grafana monitoring

🔄 CI pipeline with GitHub Actions

🚀 Simulated CD with rolling updates


## 📌 Architecture Overview

User -> UI -> FastAPI -> Model -> PostgreSQL
                      |
                  Prometheus Metrics

Airflow -> Weekly Retraining -> New Model


## 🛠 Tech Stack

Python 3.12

FastAPI

Sentence Transformers

Scikit-learn

PostgreSQL

Apache Airflow

Docker

Kubernetes

Prometheus

Grafana

GitHub Actions

GHCR (GitHub Container Registry)


## 💻 How To Run This Project Locally (From Scratch)

These steps work on macOS (including M1/M2/M3), Linux, or Windows.

### 1️⃣ Prerequisites

Install:

```
Docker Desktop (with Kubernetes enabled)

kubectl

Git
```

Verify:

```
kubectl get nodes
```

You should see:
```
Ready
```

### 2️⃣ Clone Repository
```
git clone https://github.com/Feliciasharon/Mental-Health-MLOps-NLP.git

cd Mental-Health-MLOps-NLP

```

### 3️⃣ Build Images Locally (Optional – Without CI)

If you want to run everything without GitHub CI:
```
docker build -t mental-health-mlops-nlp -f docker/Dockerfile .

docker build -t airflow-mlops -f docker/airflow.Dockerfile .
```

### 4️⃣ Deploy Infrastructure

Apply Kubernetes configs:

```
kubectl apply -f k8s/postgres-pv.yaml

kubectl apply -f k8s/postgres-pvc.yaml

kubectl apply -f k8s/postgres.yaml

kubectl apply -f k8s/deployment.yaml

kubectl apply -f k8s/service.yaml

kubectl apply -f k8s/prometheus-config.yaml

kubectl apply -f k8s/prometheus-deployment.yaml

kubectl apply -f k8s/prometheus-service.yaml

kubectl apply -f k8s/grafana.yaml

kubectl apply -f k8s/airflow.yaml
```

Check pods:

```
kubectl get pods
```

Wait until all pods show:
```
Running
```

### 5️⃣ Access the Application

Port forward API:

```
kubectl port-forward deployment/mental-health-app 8000:8000
```

Open browser:

http://localhost:8000


You should see the chat UI.

<img width="243" height="278" alt="image" src="https://github.com/user-attachments/assets/58127b16-7a7d-4a05-97e3-09a20a39e9de" />


### 📊 Monitoring

Prometheus Metrics

http://localhost:8000/metrics

<img width="463" height="116" alt="image" src="https://github.com/user-attachments/assets/1ec192e1-db5b-4c1b-8851-19950dfa9a26" />


Grafana

Port forward:
```
kubectl port-forward deployment/grafana 3000:3000
```

Open:

http://localhost:3000


Default login:
```
user: admin

password: admin

```


<img width="468" height="226" alt="image" src="https://github.com/user-attachments/assets/5d749fe4-b2e4-406e-ba68-95fea5a459c9" />

#### 🔁 Airflow Retraining

Airflow runs a scheduled retraining DAG.

Port forward:
```
kubectl port-forward deployment/airflow 8080:8080
```

Open:

http://localhost:8080

<img width="468" height="232" alt="image" src="https://github.com/user-attachments/assets/824ce327-4323-4d2a-82a5-1d8bf8f5742c" />


The DAG:

Reads new predictions from Postgres

Retrains model

Saves new classifier.pkl

Updates latest model

You can manually trigger the DAG from UI.


### 🔄 CI Pipeline

On every push to main:

GitHub Actions:

Builds Docker images

Pushes images to GHCR

Tags with:

latest

commit SHA

Images:
```
ghcr.io/feliciasharon/mental-health-mlops-nlp

ghcr.io/feliciasharon/airflow-mlops
```

### 🚀 Simulated CD (Local)

After CI finishes:

Run:

```
./deploy.sh
```

This will:

Pull latest image

Update Kubernetes deployment

Perform rolling update

You can monitor rollout:

```
kubectl rollout status deployment/mental-health-app
```

Rollback if needed:
```
kubectl rollout undo deployment/mental-health-app
```

## 🧠 Model Details

Embedding Model:

Sentence Transformer

Classifier:

Logistic Regression

Training Data:

Stored from user predictions in PostgreSQL

Retraining Strategy:

Periodic batch retraining via Airflow DAG

## 📂 Project Structure
docker/
  Dockerfile
  airflow.Dockerfile

src/
  api/app.py
  training/train.py

airflow/dags/
  retrain_weekly.py

k8s/
  deployment.yaml
  service.yaml
  postgres.yaml
  airflow.yaml
  prometheus.yaml
  grafana.yaml

requirements.txt
build.yml

## 🧩 Features Implemented

✅ NLP classification
✅ Chat-style UI
✅ Prediction logging
✅ Metrics endpoint
✅ Prometheus monitoring
✅ Grafana dashboards
✅ Scheduled retraining
✅ Docker multi-platform builds
✅ ARM64 support (Apple Silicon)
✅ CI with GitHub Actions
✅ Rolling Kubernetes deployments


Dataset link - https://www.kaggle.com/datasets/priyangshumukherjee/mental-health-text-classification-dataset?resource=download
