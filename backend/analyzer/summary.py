import pandas as pd
import numpy as np
from scipy import stats

def get_summary(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    stats_summary = []

    for col in numeric_cols:
        series = df[col].dropna()

        stats_summary.append({
            "column": col,
            "count": int(series.count()),
            "mean": round(float(series.mean()), 4),
            "median": round(float(series.median()), 4),
            "std": round(float(series.std()), 4),
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
            "q1": round(float(series.quantile(0.25)), 4),
            "q3": round(float(series.quantile(0.75)), 4),
            "skewness": round(float(stats.skew(series)), 4),
            "kurtosis": round(float(stats.kurtosis(series)), 4),
        })

    return {
        "stats_summary": stats_summary
    }