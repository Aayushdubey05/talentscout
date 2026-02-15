from fastapi import APIRouter, UploadFile, File, status, Depends, responses, HTTPException
from src.schema.user import Resume_storage
from src.models.user import Users
from typing import Annotated
from pathlib import Path
from src.services.store_file import DocumentValidator
import asyncio
import os
import shutil
import uuid
from datetime import datetime,timezone

resume_router = APIRouter()
UPLOAD_DIR = Path("C:/Users/aayus/Developer_session/talentscout/backend/resume_storage")

doc_validator = DocumentValidator(max_size=100*1024*1024)
@resume_router.post("/uploadresume",status_code=status.HTTP_201_CREATED)
async def upload_resume(file: UploadFile = File(...)):
    try:

        validation = await doc_validator.validate_file(file)

        if not validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "File validation failed",
                    "errors": validation["errors"]
                }
            )
        
        
        file_size = file.size
        file_name = file.filename 
        ## Storing of the file in the local storage 
        ## Uploading just uploaded file on the S3 bucket
        ## Assigning the key of the S3 bucket to matching User
        ## Successfull Response would be 201 status code
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_location = os.path.join(UPLOAD_DIR,unique_filename)

        # Save the file
        with open(file_location,'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "File Name": file_name,
            "content_type": file.content_type,
            "Size": file.size,
            "upload_time": datetime.now(timezone.utc).isoformat()
            }
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Pleasse try after some times") from e



