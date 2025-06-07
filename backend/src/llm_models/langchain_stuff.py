from langchain.document_loaders import PyPDFLoader
import tempfile
from fastapi import UploadFile

async def extract_pdf_text(uploaded_file: UploadFile) -> str:
    pass