from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a generated assignment file.
    """
    # Security: basic path traversal prevention
    if ".." in filename or "/" in filename or "\\" in filename:
         raise HTTPException(status_code=400, detail="Invalid filename")

    output_dir = os.path.join(os.getcwd(), "outputs")
    filepath = os.path.join(output_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(filepath, filename=filename, media_type='application/octet-stream')
