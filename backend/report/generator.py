import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

from analyzer.overview import get_overview
from analyzer.missing import get_missing
from analyzer.distributions import get_distributions
from analyzer.outliers import get_outliers
from analyzer.correlations import get_correlations
from analyzer.summary import get_summary
from report.ai_summary import generate_ai_summary

def generate_report(df: pd.DataFrame, output_path: str = "report_output.html"):
    print("Running analysis...")
    overview      = get_overview(df)
    missing       = get_missing(df)
    distributions = get_distributions(df)
    outliers      = get_outliers(df)
    correlations  = get_correlations(df)
    summary       = get_summary(df)

    print("Generating AI summary...")
    ai_summary = generate_ai_summary(overview, missing, outliers, correlations, summary)

    template_dir = os.path.join(os.path.dirname(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("template.html")

    print("Rendering template...")
    html_content = template.render(
        overview=overview,
        missing=missing,
        distributions=distributions,
        outliers=outliers,
        correlations=correlations,
        summary=summary,
        ai_summary=ai_summary
    )

    print("Saving report...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Report saved to: {output_path}")
    return output_path, html_content