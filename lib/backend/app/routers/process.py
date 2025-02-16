from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List
from app.services.file_processing import process_files

router = APIRouter()

@router.post("/process/")
async def process_files_endpoint(
    latex: List[UploadFile] = File(None),
    ppt: List[UploadFile] = File(None),
    notebook: List[UploadFile] = File(None),
):
    """
    Process uploaded files and return a merged PDF.
    """
    try:
        pdf_path = await process_files(latex, ppt, notebook)
        return FileResponse(pdf_path, media_type="application/pdf", filename="output.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))