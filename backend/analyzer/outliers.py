import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
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

def get_outliers(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    outlier_summary = []
    boxplot_charts = []

    for col in numeric_cols:
        series = df[col].dropna()

        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = series[(series < lower) | (series > upper)]

        outlier_summary.append({
            "column": col,
            "q1": round(Q1, 4),
            "q3": round(Q3, 4),
            "iqr": round(IQR, 4),
            "lower_bound": round(lower, 4),
            "upper_bound": round(upper, 4),
            "outlier_count": int(len(outliers)),
            "outlier_pct": round(len(outliers) / len(series) * 100, 2) if len(series) > 0 else 0.0
        })

        # --- Boxplot ---
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.boxplot(series, vert=False, patch_artist=True,
                   boxprops=dict(facecolor="#3498db", color="#2c3e50"),
                   medianprops=dict(color="#e74c3c", linewidth=2),
                   flierprops=dict(marker="o", color="#e74c3c", markersize=4))
        ax.set_title(f"{col} — Boxplot", fontsize=12, fontweight="bold")
        ax.set_xlabel(col)
        boxplot_charts.append({
            "column": col,
            "chart_b64": fig_to_base64(fig)
        })

    return {
        "outlier_summary": outlier_summary,
        "boxplot_charts": boxplot_charts
    }