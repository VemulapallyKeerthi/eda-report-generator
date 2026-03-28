import io
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from report.generator import generate_report

app = FastAPI(title="EDA Report Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Read CSV
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {str(e)}")

    # Validate size
    if df.empty:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    if len(df) > 100000:
        raise HTTPException(status_code=400, detail="File too large. Max 100,000 rows.")

    # Generate report
    try:
        output_path = f"temp_report_{file.filename}.html"
        _, html_content = generate_report(df, output_path=output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

    return StreamingResponse(
        io.BytesIO(html_content.encode("utf-8")),
        media_type="text/html",
        headers={"Content-Disposition": f"attachment; filename=eda_report.html"}
    )