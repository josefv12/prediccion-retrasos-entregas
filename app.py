from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import tensorflow as tf
import joblib
import json

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Predicción de retrasos")

model = tf.keras.models.load_model(BASE_DIR / "modelo_retrasos_final.keras")
preprocessor = joblib.load(BASE_DIR / "preprocesador_retrasos_final.joblib")

with open(BASE_DIR / "configuracion_modelo.json", "r", encoding="utf-8") as f:
    config = json.load(f)

THRESHOLD = float(config["threshold"])


@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok", "model": config["model_name"]}


@app.post("/predict")
async def predict(payload: dict):
    try:
        row = pd.DataFrame([{
            "Shipping Mode": payload["shipping_mode"],
            "Days for shipment (scheduled)": float(payload["scheduled_days"]),
            "Days for shipping (real)": float(payload["real_days"]),
            "Customer Segment": payload["customer_segment"],
            "Type": payload["order_type"]
        }])
        X = preprocessor.transform(row[config["features"]])
        probability = float(model.predict(X, verbose=0)[0][0])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=f"Datos de entrada inválidos: {exc}") from exc

    prediction = int(probability >= THRESHOLD)
    return {
        "probability": probability,
        "prediction": prediction,
        "result": "RETRASO" if prediction else "NO RETRASO",
        "threshold": THRESHOLD
    }
