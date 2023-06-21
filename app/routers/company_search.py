from fastapi import APIRouter, Depends, status, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter(
    prefix="/Companies search",
    tags=['Company search']
)


@router.post("/upload-file/")
async def upload_companies_file(file: UploadFile, db:Session = Depends(get_db)):
    return {"filename": file.filename, 'dataset_id':"temp"}


@router.get("/get-results/{datset_id}")
async def get_results(dataset_id:str, db:Session = Depends(get_db)):
    pass