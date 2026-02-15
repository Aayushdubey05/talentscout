import requests
from fastapi import responses
import aiofiles
import asyncio
import os
import shutil
from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = "backend/resume_storage"
os.makedirs(UPLOAD_DIR,exist_ok=True)
class DocumentValidator:
    def __init__(self, max_size : int = 50 * 1024 * 1024):
        self.max_size = max_size
        self.allowed_extension = {'.pdf','.doc','.docx'}

    async def validate_file(self, file:UploadFile) -> dict:
        results = {"valid": True, "errors": []}

        if not file.filename or file.filename.string() == "":
            results["valid"] = False
            results["errors"].append("No file selected")

        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extension:
            results["valid"] = False
            results["errors"].append(
                f"File Extension '{file_ext}' not allowed. Use: .pdf, .doc, .docx"
            )
        content = await file.read()
        await file.seek(0)

        file_size = len(content)
        if file_size > self.max_size:
            results["valid"] = False
            results["errors"].append(
                f"File too larger ({file_size:,} bytes. Maximum: {self.max_size:,} bytes)"
            )
        
        return results
    