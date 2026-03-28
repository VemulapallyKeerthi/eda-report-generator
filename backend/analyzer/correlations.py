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

def get_correlations(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return {
            "has_correlations": False,
            "top_pairs": [],
            "heatmap_b64": None
        }

    corr_matrix = numeric_df.corr()

    # --- Top correlated pairs (excluding self-correlations) ---
    pairs = []
    cols = corr_matrix.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append({
                "col_a": cols[i],
                "col_b": cols[j],
                "correlation": round(corr_matrix.loc[cols[i], cols[j]], 4)
            })

    pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    top_pairs = pairs[:10]

    # --- Heatmap ---
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        ax=ax
    )
    ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
    heatmap_b64 = fig_to_base64(fig)

    return {
        "has_correlations": True,
        "top_pairs": top_pairs,
        "heatmap_b64": heatmap_b64
    }