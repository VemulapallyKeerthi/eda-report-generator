import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import base64
from io import BytesIO

matplotlib.use("Agg")

def fig_to_base64(fig) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded

def get_distributions(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    numeric_charts = []
    categorical_charts = []

    # --- Numeric: Histograms ---
    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color="#3498db")
        ax.set_title(f"{col} — Distribution", fontsize=12, fontweight="bold")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        numeric_charts.append({
            "column": col,
            "chart_b64": fig_to_base64(fig)
        })

    # --- Categorical: Bar Charts (top 10 values) ---
    for col in categorical_cols:
        top_values = df[col].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(top_values.index.tolist(), top_values.values.tolist(), color="#2ecc71")
        ax.set_title(f"{col} — Top Values", fontsize=12, fontweight="bold")
        ax.set_xlabel("Count")
        ax.invert_yaxis()
        categorical_charts.append({
            "column": col,
            "chart_b64": fig_to_base64(fig)
        })

    return {
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "numeric_charts": numeric_charts,
        "categorical_charts": categorical_charts
    }