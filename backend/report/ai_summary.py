import json
from groq import Groq

def generate_ai_summary(overview: dict, missing: dict, outliers: dict, correlations: dict, summary: dict) -> str:

    stats_text = f"""
Dataset: {overview['num_rows']} rows x {overview['num_columns']} columns
Memory: {overview['memory_usage_kb']} KB
Duplicates: {overview['duplicate_rows']}

Missing Data:
- Total missing: {missing['total_missing_pct']}%
- Columns with missing: {[col['name'] + ' (' + str(col['null_pct']) + '%)' for col in missing['columns_with_missing']]}

Outliers (IQR method):
{json.dumps([{'column': o['column'], 'outlier_pct': o['outlier_pct']} for o in outliers['outlier_summary'] if o['outlier_count'] > 0], indent=2)}

Top Correlations:
{json.dumps(correlations['top_pairs'][:5] if correlations['has_correlations'] else [], indent=2)}

Statistical Highlights:
{json.dumps([{'column': s['column'], 'mean': s['mean'], 'median': s['median'], 'skewness': s['skewness']} for s in summary['stats_summary']], indent=2)}
"""

    client = Groq()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": f"""You are a data analyst. Based on the dataset statistics below, write a concise executive summary (3-5 sentences) highlighting the most important findings: data quality issues, notable distributions, significant correlations, and outlier concerns. Be specific and actionable.

{stats_text}

Write only the summary paragraph, no headers or bullet points."""
            }
        ]
    )

    return response.choices[0].message.content