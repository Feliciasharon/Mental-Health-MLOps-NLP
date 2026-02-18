'''import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer

# 1️⃣ Load dataset
df = pd.read_csv("data/mental_health.csv")

texts = df["text"].astype(str).tolist()
labels = df["status"]

# 2️⃣ Load MiniLM model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 3️⃣ Generate embeddings
embeddings = embedder.encode(texts, show_progress_bar=True)

# 4️⃣ Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    embeddings, labels, test_size=0.2, random_state=42
)

# 5️⃣ Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print("Accuracy:", accuracy)

# 6️⃣ Track in MLflow
mlflow.set_experiment("mental_health_classification")

with mlflow.start_run():
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(clf, "classifier")

# 7️⃣ Save locally
joblib.dump(clf, "classifier.pkl")
embedder.save("embedder")

print("Training complete.")
'''


import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer
import psycopg2
import numpy as np
from datetime import datetime
import os

# Connect to Postgres
conn = psycopg2.connect(
    host="postgres-service",
    database="mldb",
    user="mluser",
    password="mlpassword"
)

df = pd.read_sql("SELECT text, prediction FROM predictions", conn)
conn.close()

if len(df) == 0:
    print("No data available for retraining.")
    exit()

'''BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "classifier.pkl")
EMBEDDER_PATH = os.path.join(BASE_DIR, "embedder")

embedder = SentenceTransformer(EMBEDDER_PATH)'''

embedder = SentenceTransformer("/opt/airflow/mlops/embedder")
BASE_DIR = "/opt/airflow/mlops"

X = embedder.encode(df["text"].tolist())
y = df["prediction"].tolist()

clf = LogisticRegression()

unique_classes = np.unique(y)

if len(unique_classes) < 2:
    print("Not enough class diversity. Skipping retraining.")
    exit(0)

clf.fit(X, y)

timestamp = datetime.utcnow().strftime("%Y%m%d%H%M")
model_path = f"{BASE_DIR}/models/classifier_{timestamp}.pkl"

os.makedirs(f"{BASE_DIR}/models", exist_ok=True)
joblib.dump(clf, model_path)

# Update latest model
joblib.dump(clf, f"{BASE_DIR}/classifier.pkl")

print(f"Model saved at {model_path}")

print("Model retrained successfully.")
