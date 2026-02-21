import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse
from io import BytesIO
from core.formatter_pipeline import ExcelPipeline
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.post("/format")
async def format_excel(file: UploadFile = File(...)):
    contents = await file.read()
    input_buffer = BytesIO(contents)
    # Example: column order can be passed as a query param or hardcoded
    pipeline = ExcelPipeline(column_order=None)  # Set column_order as needed
    output_buffer = pipeline.process(input_buffer)
    output_buffer.seek(0)
    return StreamingResponse(output_buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=formatted_{file.filename}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)