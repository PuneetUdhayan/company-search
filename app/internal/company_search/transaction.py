from typing import Optional

from pandas import DataFrame
from sqlalchemy.orm import Session

from app.database.models import Companies, Datasets, DatasetState


def insert_dataset(dataset_name: str, db: Session):
    dataset = Datasets(dataset_name=dataset_name, status=DatasetState.PROCESSING.value)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


def insert_companies(df: DataFrame, db: Session):
    dict_data = df.to_dict(orient="records")
    data = [Companies(**i) for i in dict_data]
    db.bulk_save_objects(data)
    db.commit()


def get_dataset(dataset_id: str, db: Session) -> DatasetState:
    dataset = db.query(Datasets).filter(Datasets.id == dataset_id).first()
    if dataset:
        dataset.status = DatasetState(dataset.status)
        return dataset


def get_companies(dataset_id: str, db: Session):
    return db.query(Companies).filter(Companies.dataset_id == dataset_id).all()


def update_dataset_state(
    dataset_id: str,
    status: DatasetState,
    db: Session,
    error_message: Optional[str] = None,
):
    update_dict = {"status": status.value}
    if error_message:
        update_dict["error_message"] = error_message
    db.query(Datasets).filter(Datasets.id == dataset_id).update(update_dict)
    db.commit()


def find_company_by_name(company_name: str, db: Session):
    return (
        db.query(Companies)
        .join(Datasets)
        .filter(
            Companies.company == company_name,
            Datasets.status == DatasetState.COMPLETED.value,
        )
        .first()
    )
