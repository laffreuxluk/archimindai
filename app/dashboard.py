import plotly.express as px
import pandas as pd

def create_dashboard(df, output_path="output/dashboard.html"):
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_cols) < 2:
        print("Nombre de colonnes numériques insuffisant pour créer un dashboard.")
        return
    fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title="Dashboard - Scatter Plot")
    fig.write_html(output_path)
    print(f"Dashboard sauvegardé dans {output_path}")
