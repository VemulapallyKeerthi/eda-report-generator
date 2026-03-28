import pandas as pd
from analyzer.summary import get_summary

df = pd.read_csv("test.csv")
result = get_summary(df)

print("Statistical Summary:")
for col in result["stats_summary"]:
    print(f"\n  {col['column']}")
    print(f"    Count:    {col['count']}")
    print(f"    Mean:     {col['mean']}")
    print(f"    Median:   {col['median']}")
    print(f"    Std:      {col['std']}")
    print(f"    Min/Max:  {col['min']} / {col['max']}")
    print(f"    Q1/Q3:    {col['q1']} / {col['q3']}")
    print(f"    Skewness: {col['skewness']}")
    print(f"    Kurtosis: {col['kurtosis']}")