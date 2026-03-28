import pandas as pd
from analyzer.missing import get_missing

df = pd.read_csv("test.csv")
result = get_missing(df)

print(f"Total missing cells: {result['total_missing_cells']}")
print(f"Overall missing: {result['total_missing_pct']}%")
print("\nColumns with missing values:")
for col in result["columns_with_missing"]:
    print(f"  {col['name']} — {col['null_count']} missing ({col['null_pct']}%)")

if result["heatmap_b64"]:
    print("\nHeatmap generated successfully ✓")