from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS  # Permite peticiones desde el frontend

app = Flask(__name__)
CORS(app)  # Habilita CORS para que el frontend pueda acceder

# Cargar el modelo entrenado y las métricas
try:
    model, eval_metrics = joblib.load("model.pkl")
    print("Modelo cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None  # Evita que Flask crashee si el modelo no se encuentra
    eval_metrics = None

@app.route("/")
def home():
    return "API de Predicción de Tiempo de Evacuación está en funcionamiento."

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Modelo no cargado"}), 500

    data = request.get_json()
    
    try:
        # Extraer las características desde la petición JSON
        features = np.array(data["features"]).reshape(1, -1)
        
        # Hacer la predicción con el modelo cargado
        prediction = model.predict(features)
        
        return jsonify({"prediction": float(prediction[0])})
    
    except Exception as e:
        return jsonify({"error": f"Error en la predicción: {str(e)}"}), 400

@app.route("/metrics", methods=["GET"])
def get_metrics():
    if eval_metrics is None:
        return jsonify({"error": "Métricas no disponibles"}), 500
    return jsonify(eval_metrics)

if __name__ == "__main__":
    app.run(debug=True, port=5000)