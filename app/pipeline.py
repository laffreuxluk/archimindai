import os
import pandas as pd
import dask.dataframe as dd
import numpy as np
import joblib
import logging
from config import OUTPUT_DIR
from app.cleaning import clean_data
from app.models import select_best_model
from app.report import generate_pptx_report, generate_html_report
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def run_analysis(file_path):
    logging.info(f"Début de l'analyse pour {file_path}")
    try:
        with open(file_path, 'r') as f:
            n_lines = sum(1 for _ in f)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier : {e}")
        return

    if n_lines < 500000:
        df = pd.read_csv(file_path)
    else:
        df = dd.read_csv(file_path).compute()

    df = clean_data(df)
    df = normalize_data(df)
    model, predictions = classify_data(df)
    anomalies = detect_anomalies(df)

    from app.ai_commentary import generate_commentary
    commentary = generate_commentary(df) if generate_commentary is not None else ""

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    pptx_path = os.path.join(OUTPUT_DIR, "ArchiMindAI_Report.pptx")
    html_path = os.path.join(OUTPUT_DIR, "ArchiMindAI_Report.html")
    generate_pptx_report(df, predictions, anomalies, commentary, output_path=pptx_path)
    generate_html_report(df, predictions, anomalies, commentary, output_path=html_path)

    from app.supabase_storage import store_file_to_supabase
    store_file_to_supabase(file_path)

    model_path = os.path.join(OUTPUT_DIR, "best_model.pkl")
    joblib.dump(model, model_path)
    logging.info(f"Analyse terminée pour {file_path}")

def normalize_data(df):
    from sklearn.preprocessing import StandardScaler
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def classify_data(df):
    from app.models import select_best_model
    model = select_best_model(df)
    predictions = model.predict(df)
    return model, predictions

def detect_anomalies(df):
    numeric_data = df.select_dtypes(include=["float64", "int64"])
    iso = IsolationForest(contamination=0.05, random_state=42)
    iso.fit(numeric_data)
    iso_preds = iso.predict(numeric_data)
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    lof_preds = lof.fit_predict(numeric_data)
    anomalies = df[iso_preds == -1]
    return anomalies
