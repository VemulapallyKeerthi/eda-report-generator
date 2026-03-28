import pandas as pd
from analyzer.correlations import get_correlations

df = pd.read_csv("test.csv")
result = get_correlations(df)

print(f"Has correlations: {result['has_correlations']}")
print(f"Heatmap generated: {'Yes' if result['heatmap_b64'] else 'No'}")

print("\nTop Correlated Pairs:")
for pair in result["top_pairs"]:
    print(f"  {pair['col_a']} vs {pair['col_b']} → {pair['correlation']}")