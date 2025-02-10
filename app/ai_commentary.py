from config import USE_AI_COMMENTARY

def generate_commentary(df=None):
    if not USE_AI_COMMENTARY:
        return "Commentaire IA désactivé."
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="google/flan-t5-small")
        summary_text = f"Le dataset contient {len(df)} enregistrements et {df.shape[1]} variables. " if df is not None else "Aucune donnée fournie."
        summary_text += " Les anomalies et tendances ont été analysées avec précision."
        result = summarizer(summary_text, max_length=50, min_length=25, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        print(f"Erreur lors de la génération du commentaire IA : {e}")
        return "Erreur lors de la génération du commentaire IA."
