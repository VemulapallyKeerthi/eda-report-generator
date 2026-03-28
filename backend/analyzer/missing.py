import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import base64
from io import BytesIO

matplotlib.use("Agg")  # Non-interactive backend, required for servers

def fig_to_base64(fig) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded

def get_missing(df: pd.DataFrame) -> dict:
    null_counts = df.isnull().sum()
    null_pcts = (df.isnull().mean() * 100).round(2)

    # Only columns that actually have missing values
    missing_cols = null_counts[null_counts > 0]

    columns_with_missing = [
        {
            "name": col,
            "null_count": int(null_counts[col]),
            "null_pct": float(null_pcts[col])
        }
        for col in missing_cols.index
    ]

    heatmap_b64 = None
    barplot_b64 = None

    if len(missing_cols) > 0:
        # --- Heatmap ---
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.heatmap(
            df[missing_cols.index].isnull(),
            cbar=False,
            yticklabels=False,
            cmap="viridis",
            ax=ax
        )
        ax.set_title("Missing Value Heatmap", fontsize=14, fontweight="bold")
        ax.set_xlabel("Columns")
        heatmap_b64 = fig_to_base64(fig)

        # --- Bar Chart ---
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(
            missing_cols.index.tolist(),
            null_pcts[missing_cols.index].tolist(),
            color="#e74c3c"
        )
        ax.set_xlabel("Missing %")
        ax.set_title("Missing Data by Column", fontsize=14, fontweight="bold")
        ax.axvline(x=50, color="black", linestyle="--", linewidth=0.8, label="50% line")
        ax.legend()
        barplot_b64 = fig_to_base64(fig)

    return {
        "total_missing_cells": int(null_counts.sum()),
        "total_missing_pct": round(null_counts.sum() / df.size * 100, 2),
        "columns_with_missing": columns_with_missing,
        "heatmap_b64": heatmap_b64,
        "barplot_b64": barplot_b64
    }