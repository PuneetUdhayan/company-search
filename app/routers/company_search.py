from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    UploadFile,
    BackgroundTasks,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models import DatasetState
from app.internal.company_search import controller
from app.internal.company_search import exceptions


router = APIRouter(prefix="/companies-search", tags=["Company search"])


@router.post("/upload-file/")
def upload_companies_file(file: UploadFile, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        dataset_id = controller.upload_dataset(
            filename=file.filename, file_content=file.file.read(), db=db
        )
        background_tasks.add_task(controller.assign_companies, dataset_id=dataset_id, db=db)
        return {"dataset_id": dataset_id}
    except exceptions.FileExceptions as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get-results/{datset_id}")
def get_results(dataset_id: str, db: Session = Depends(get_db)):
    try:
        result = controller.fetch_results(dataset_id=dataset_id, db=db)
        if result.success:
            return FileResponse(path=result.file_path, filename=result.file_name)
        else:
            return {
                "job_status": "processing"
                if result.dataset_status == DatasetState.PROCESSING
                else "error",
                "error_message": result.error_message,
            }
    except exceptions.DatasetDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No dataset found for ID {dataset_id}",
        )
