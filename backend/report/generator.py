import pandas as pd
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os

from analyzer.overview import get_overview
from analyzer.missing import get_missing
from analyzer.distributions import get_distributions
from analyzer.outliers import get_outliers
from analyzer.correlations import get_correlations
from analyzer.summary import get_summary
from report.ai_summary import generate_ai_summary

def generate_report(df: pd.DataFrame, output_path: str = "report_output.pdf"):
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

    print("Generating PDF...")
    with open(output_path, "wb") as f:
        pisa_status = pisa.CreatePDF(html_content, dest=f)

    if pisa_status.err:
        print(f"PDF generation error: {pisa_status.err}")
    else:
        print(f"Report saved to: {output_path}")

    return output_path