import pandas as pd
from analyzer.outliers import get_outliers

df = pd.read_csv("test.csv")
result = get_outliers(df)

print("Outlier Summary:")
for col in result["outlier_summary"]:
    print(f"  {col['column']} — {col['outlier_count']} outliers ({col['outlier_pct']}%) | bounds: [{col['lower_bound']}, {col['upper_bound']}]")

print(f"\nBoxplots generated: {len(result['boxplot_charts'])}")
for chart in result["boxplot_charts"]:
    print(f"  ✓ {chart['column']}")