from typing import Optional

from pydantic import BaseModel

from app.database.models import DatasetState


class FileResponse(BaseModel):
    success:bool
    dataset_status: DatasetState
    error_message: Optional[str]
    file_name: Optional[str]
    file_path: Optional[str]