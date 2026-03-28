import pandas as pd
from report.generator import generate_report

df = pd.read_csv("test.csv")
generate_report(df, output_path="test_report.pdf")