from fastapi import APIRouter, Depends, status, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.internal.company_search import controller
from app.internal.company_search import exceptions


router = APIRouter(prefix="/Companies search", tags=["Company search"])


@router.post("/upload-file/")
def upload_companies_file(file: UploadFile, db: Session = Depends(get_db)):
    try:
        dataset_id = controller.upload_dataset(
            filename=file.filename, file_content=file.file.read(), db=db
        )
        return {"dataset_id": dataset_id}
    except exceptions.FileExceptions as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get-results/{datset_id}")
def get_results(dataset_id: str, db: Session = Depends(get_db)):
    pass
