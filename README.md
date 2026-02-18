

Dataset link - https://www.kaggle.com/datasets/priyangshumukherjee/mental-health-text-classification-dataset?resource=download

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 src/training/train.py

mlflow ui

Go to:

http://localhost:5000


You’ll see experiment tracking.

uvicorn src.api.app:app --reload

go to http://127.0.0.1:8000/docs

docker run -p 9090:9090 \
-v "$(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml" \
prom/prometheus

Visit:

http://localhost:9090


Query:

prediction_requests_total


To check results:

✅ Now Generate Traffic

Run this 3–5 times:

curl -X POST http://127.0.0.1:8000/predict \
-H "Content-Type: application/json" \
-d '{"text":"I feel anxious and stressed"}'


Then refresh:

http://127.0.0.1:8000/metrics


You should now see:

prediction_requests_total 5.0

✅ Now Check Prometheus

Go to:

http://localhost:9090


Query:

prediction_requests_total


Click Execute.

You should now see the value > 0.


▶ Build & Run Docker
docker build -t mental-health-mlops -f docker/Dockerfile .
docker run -p 8000:8000 mental-health-mlops

to shutdown docker and restart

docker-compose down
docker-compose up --build


Create Kubernetes Cluster
kind create cluster


Verify:

kubectl cluster-info

kind load docker-image mlops-app

kubectl apply -f k8s/deployment.yaml

kubectl get pods

kubectl apply -f k8s/service.yaml

kubectl port-forward service/mental-health-service 8000:8000

#scaling

kubectl scale deployment mental-health-app --replicas=4

kubectl apply -f k8s/prometheus-config.yaml
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/prometheus-service.yaml

kubectl port-forward service/prometheus-service 9090:9090

in another terminal:
kubectl port-forward service/mental-health-service 8000:8000


kubectl apply -f k8s/grafana.yaml
kubectl get pods

kubectl port-forward service/grafana-service 3000:3000


Rebuild & Reload App (app.py)

If you changed bootstrap_servers:

docker build -t mlops-app:latest -f docker/Dockerfile .
kind load docker-image mlops-app:latest
kubectl rollout restart deployment mental-health-app


Start Kafka in Docker (KRaft Mode)

Run this exact command:

docker run -d \
  --name kafka \
  -p 9092:9092 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk \
  confluentinc/cp-kafka:7.5.0


kubectl apply -f k8s/kafka-consumer.yaml
kubectl rollout restart deployment kafka-consumer


kubectl apply -f k8s/postgres.yaml
kubectl port-forward service/postgres-service 5432:5432

in another terminal to check reach:

kubectl exec -it deployment/postgres -- psql -U mluser -d mldb

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    text TEXT,
    prediction TEXT,
    probabilities JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


SELECT * FROM predictions;
\q

kubectl apply -f k8s/airflow.yaml

kubectl port-forward service/airflow-service 8080:8080



docker build -t mlops-airflow:v1.0.0 -f airflow/Dockerfile .

kind load docker-image mlops-airflow:v1.0.0
kubectl rollout restart deployment airflow

lsof -i :8080
 kill -9 47522





🚨 STEP 1 — Delete Everything Cleanly

From your project root:

kubectl delete deployment --all
kubectl delete service --all
kubectl delete pvc --all
kubectl delete pv --all


If you want to be extra clean (optional):

kubectl delete configmap --all
kubectl delete secret --all


Now verify:

kubectl get all


You should see basically nothing running.

🧱 STEP 2 — Rebuild Images (Fresh)

From project root:

Rebuild FastAPI app
docker build -t mlops-app -f docker/Dockerfile .

Rebuild Airflow image
docker build -t airflow-mlops:v1.0.0 -f docker/airflow.Dockerfile .

🚀 STEP 3 — Deploy In Correct Order

Order matters.

1️⃣ Postgres (storage first)
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres.yaml


Wait until:

kubectl get pods


Postgres shows Running.

2️⃣ FastAPI App
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml


Check:

kubectl get pods


Then test health:

kubectl port-forward service/mental-health-service 8000:8000


Visit:

http://localhost:8000/health


Must return:

{"status":"ok"}


If not — stop here and fix before continuing.

3️⃣ Prometheus
kubectl apply -f k8s/prometheus-config.yaml
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/prometheus-service.yaml

4️⃣ Grafana
kubectl apply -f k8s/grafana.yaml

5️⃣ Airflow
kubectl apply -f k8s/airflow.yaml


Wait until:

kubectl get pods


Airflow should show Running.

🧪 STEP 4 — Verify Everything
FastAPI
localhost:8000

Airflow
kubectl port-forward service/airflow-service 8080:8080

http://localhost:8080

Prometheus
kubectl port-forward service/prometheus-service 9090:9090

Grafana
kubectl port-forward service/grafana-service 3000:3000



kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=feliciasharon \
  --docker-password=<secret key> \
  --docker-email=in.felicia.sharon@gmail.com


#links

http://localhost:3000 - grafana
http://localhost:9090 - prometheus query - sum(prediction_requests_total)
http://localhost:8000/docs - fastapi predict
http://localhost:8000/metrics - raw metrics (prediction_requests_total)
