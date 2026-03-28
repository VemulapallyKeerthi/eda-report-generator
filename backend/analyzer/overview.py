import pandas as pd

def get_overview(df: pd.DataFrame) -> dict:
    """
    Returns high-level dataset overview.
    """
    overview = {
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
        "columns": []
    }

    for col in df.columns:
        overview["columns"].append({
            "name": col,
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isnull().sum()),
            "null_pct": round(df[col].isnull().mean() * 100, 2),
            "unique_count": int(df[col].nunique())
    })

    return overview