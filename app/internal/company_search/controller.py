import uuid
from io import BytesIO

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from . import exceptions, transaction


def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]


def read_file(filename:str, file_content) -> pd.DataFrame:
    file_extension = get_file_extension(filename)
    if file_extension == "xlsx":
        return pd.read_excel(BytesIO(file_content))
    else:
        return pd.read_csv(BytesIO(file_content))


def make_dataframe_headers_lowercase(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=lambda x: x.lower())


def file_type_validation(filename: str, file_content):
    file_extension = get_file_extension(filename)
    if file_extension not in ("xlsx", "csv"):
        raise exceptions.FileFormatNotSupported()


def file_corruption_check(filename: str, file_content):
    try:
        read_file(filename, file_content)
    except Exception as e:
        raise exceptions.FileCorrupted()


def file_header_check(filename: str, file_content):
    df = read_file(filename, file_content)
    df = make_dataframe_headers_lowercase(df)
    if "companies" not in df.columns:
        raise exceptions.FileHeadersIncorrect()


def file_size_check(filename: str, file_content):
    df = read_file(filename, file_content)
    if df.shape[0] > 10:
        raise exceptions.FileTooLarge()


def file_validations(filename: str, file_content):
    validations = [
        file_type_validation,
        file_corruption_check,
        file_header_check,
        file_size_check,
    ]
    for validation in validations:
        validation(filename, file_content)


def upload_dataset(filename: str, file_content, db: Session) -> str:
    # Run validations
    file_validations(filename, file_content)
    dataset_id = str(uuid.uuid4())
    return dataset_id


def fetch_results(dataset_id: str, db: Session):
    pass
