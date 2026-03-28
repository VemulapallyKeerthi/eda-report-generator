import pandas as pd
from analyzer.overview import get_overview

df = pd.read_csv("test.csv")
result = get_overview(df)

print(f"Rows: {result['num_rows']}, Columns: {result['num_columns']}")
print(f"Duplicates: {result['duplicate_rows']}")
print(f"Memory: {result['memory_usage_kb']} KB")
print("\nColumn Details:")
for col in result["columns"]:
    print(f"  {col['name']} | {col['dtype']} | nulls: {col['null_percent']}%")