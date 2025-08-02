import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_qr_from_image

app = FastAPI()

# Set CORS to only allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-netlify-site.netlify.app"],
    allow_methods=["POST"],
    allow_headers=["*"],
    allow_credentials=False  # Set true if you require cookies/auth later
)

@app.post("/scan/")
async def scan_qr_api(file: UploadFile = File(...)):
    # Sanitize filename
    safe_name = os.path.basename(file.filename)
    suffix = Path(safe_name).suffix or '.png'

    # Save upload to a temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        shutil.copyfileobj(file.file, tmp)
        tmp.flush()
        tmp_path = tmp.name
    finally:
        tmp.close()
        file.file.close()

    try:
        result = scan_qr_from_image(tmp_path)
        if isinstance(result, list) and not result:
            raise HTTPException(status_code=404, detail="No QR code detected")
        return result
    finally:
        os.remove(tmp_path)
