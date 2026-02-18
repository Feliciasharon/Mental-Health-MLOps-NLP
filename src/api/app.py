
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import joblib
from sentence_transformers import SentenceTransformer
import psycopg2
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time
import os


app = FastAPI()

REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total number of prediction requests"
)

REQUEST_LATENCY = Histogram(
    "prediction_request_duration_seconds",
    "Time spent processing prediction request"
)



@app.get("/health")
def health():
    return {"status": "ok"}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "classifier.pkl")
EMBEDDER_PATH = os.path.join(BASE_DIR, "embedder")
clf = joblib.load(MODEL_PATH)
embedder = SentenceTransformer(EMBEDDER_PATH)
# Load model + embedder once
#clf = joblib.load("/opt/airflow/mlops/classifier.pkl")
#embedder = SentenceTransformer("/opt/airflow/mlops/embedder")
#clf = joblib.load("classifier.pkl")
#embedder = SentenceTransformer("embedder")

def save_to_db(text, prediction):
    conn = psycopg2.connect(
        host="postgres-service",
        database="mldb",
        user="mluser",
        password="mlpassword"
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (text, prediction) VALUES (%s, %s)",
        (text, prediction)
    )
    conn.commit()
    conn.close()

def render_chat(user_text=None, prediction=None):

    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
<title>InstaChat</title>
<style>

body {{
    margin: 0;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}}

.phone {{
    width: 390px;
    height: 750px;
    background: #121212;
    border-radius: 35px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.6);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.header {{
    background: #1c1c1c;
    padding: 15px;
    text-align: center;
    color: white;
    font-weight: 600;
    font-size: 16px;
    border-bottom: 1px solid #2a2a2a;
}}

.chat-area {{
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.message {{
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 22px;
    font-size: 14px;
    line-height: 1.4;
    animation: fadeIn 0.25s ease-in;
}}

.bot {{
    background: #262626;
    color: white;
    align-self: flex-start;
}}

.user {{
    background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
    color: white;
    align-self: flex-end;
}}

.prediction {{
    background: #262626;
    color: white;
    align-self: flex-start;
}}

.prediction span {{
    font-weight: bold;
    color: #4fc3f7;
}}

.input-bar {{
    padding: 10px;
    background: #1c1c1c;
    display: flex;
    align-items: center;
    border-top: 1px solid #2a2a2a;
}}

input {{
    flex: 1;
    background: #2a2a2a;
    border: none;
    outline: none;
    padding: 10px 15px;
    border-radius: 25px;
    color: white;
    font-size: 14px;
}}

button {{
    background: none;
    border: none;
    color: #3897f0;
    font-weight: 600;
    margin-left: 10px;
    font-size: 14px;
    cursor: pointer;
}}

button:hover {{
    opacity: 0.8;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(5px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

::-webkit-scrollbar {{
    width: 0px;
}}

</style>
</head>

<body>

<div class="phone">

    <div class="header">
        mental.health
    </div>

    <div class="chat-area">
        <div class="message bot">Hey 👋 How are you feeling today?</div>
        <div class="message bot">You can tell me anything.</div>

        {f'<div class="message user">{user_text}</div>' if user_text else ''}
        {f'<div class="message prediction">Oh looks like you are <span>{prediction}</span></div>' if prediction else ''}
    </div>

    <form method="post" action="/predict" class="input-bar">
        <input type="text" name="text" placeholder="Message..." required>
        <button type="submit">Send</button>
    </form>

</div>

</body>
</html>
""")


@app.get("/", response_class=HTMLResponse)
def chat_ui():
    return render_chat()


@app.post("/predict", response_class=HTMLResponse)
def predict(text: str = Form(...)):
    
    REQUEST_COUNT.inc()
    start_time = time.time()

    embedding = embedder.encode([text])
    prediction = clf.predict(embedding)[0]

    save_to_db(text, prediction)

    REQUEST_LATENCY.observe(time.time() - start_time)

    return render_chat(user_text=text, prediction=prediction)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
