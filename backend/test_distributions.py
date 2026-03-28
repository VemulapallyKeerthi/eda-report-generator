import pandas as pd
from analyzer.distributions import get_distributions

df = pd.read_csv("test.csv")

try:
    result = get_distributions(df)
    print(f"Numeric columns: {result['numeric_columns']}")
    print(f"Categorical columns: {result['categorical_columns']}")

    print(f"\nNumeric charts generated: {len(result['numeric_charts'])}")
    for chart in result["numeric_charts"]:
        print(f"  ✓ {chart['column']}")

    print(f"\nCategorical charts generated: {len(result['categorical_charts'])}")
    for chart in result["categorical_charts"]:
        print(f"  ✓ {chart['column']}")

except Exception as e:
    import traceback
    traceback.print_exc()