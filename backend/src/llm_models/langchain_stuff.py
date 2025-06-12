# from langchain.document_loaders import PyPDFLoader
import tempfile
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader



async def extract_pdf_text(uploaded_file: UploadFile) -> str:
    loader = PyPDFLoader(uploaded_file)
    page = []
    async for page in loader.alazy_load():
        page.append(page)
    
    print(f"{page[0].metadata}\n")
    print(page[0].page_content)
    return page[0].page_content

