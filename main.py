from fastapi import FastAPI, UploadFile, File, HTTPException
from markitdown import MarkItDown
import tempfile, os, pathlib

app = FastAPI(title="MarkItDown Service")
md = MarkItDown(enable_plugins=False)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".pptx", ".csv"}

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    ext = pathlib.Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415, 
            detail=f"Tipo de archivo no soportado: {ext}"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = md.convert_local(tmp_path)
        return {
            "filename": file.filename,
            "markdown": result.text_content
        }
    finally:
        os.unlink(tmp_path)

@app.get("/health")
def health():
    return {"status": "ok"}