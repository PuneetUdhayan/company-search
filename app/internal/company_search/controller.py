import os
import uuid
import requests
from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from app.database.models import DatasetState
from . import exceptions, transaction, schemas


def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]


def read_file(filename: str, file_content) -> pd.DataFrame:
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


def file_corruption_validation(filename: str, file_content):
    try:
        read_file(filename, file_content)
    except Exception as e:
        raise exceptions.FileCorrupted()


def file_header_validation(filename: str, file_content):
    df = read_file(filename, file_content)
    df = make_dataframe_headers_lowercase(df)
    if "company" not in df.columns:
        raise exceptions.FileHeadersIncorrect()


def file_size_validation(filename: str, file_content):
    df = read_file(filename, file_content)
    if df.shape[0] > 10:
        raise exceptions.FileTooLarge()


def file_validations(filename: str, file_content):
    # Need to make this function a class to easily share data
    validations = [
        file_type_validation,
        file_corruption_validation,
        file_header_validation,
        file_size_validation,
    ]
    for validation in validations:
        validation(filename, file_content)


def get_company_url(company_name: str) -> str:
    subscription_key = os.environ.get(
        "BING_API_KEY", "c33936083a5240719da4a4935bd7f59b"
    )
    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    # Query term(s) to search for.
    query = f"{company_name} site:linkedin.com/company/"

    # Construct a request
    mkt = "en-US"
    params = {"q": query, "mkt": mkt, "count": 1}
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    # Call the API
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code != 200:
        raise exceptions.BingApiNotReachable()

    company_url = "Not found"

    # Need to clean up the use of try catch here
    try:
        company_url = response.json()["webPages"]["value"][0]["displayUrl"]
        if "linkedin.com/company/" not in company_url:
            raise Exception("Company not found")
    except Exception as e:
        pass

    return company_url


def upload_dataset(filename: str, file_content, db: Session) -> str:
    file_validations(filename, file_content)
    df = read_file(filename=filename, file_content=file_content)
    dataset_id = transaction.insert_dataset(dataset_name=filename, db=db).id
    df["dataset_id"] = dataset_id
    transaction.insert_companies(df=df, db=db)
    return dataset_id


def assign_companies(dataset_id: str, db: Session):
    try:
        companies_data = transaction.get_companies(dataset_id=dataset_id, db=db)

        for company in companies_data:
            company_info = transaction.find_company_by_name(
                company_name=company.company, db=db
            )
            if company_info:
                company.linkedin_url = company_info.linkedin_url
            else:
                company.linkedin_url = get_company_url(company_name=company.company)

        db.commit()

        transaction.update_dataset_state(
            dataset_id=dataset_id,
            status=DatasetState.COMPLETED,
            db=db
        )

    except Exception as e:
        transaction.update_dataset_state(
            dataset_id=dataset_id,
            status=DatasetState.ERROR,
            db=db,
            error_message=str(e),
        )


def fetch_results(dataset_id: str, db: Session) -> schemas.FileResponse:
    dataset = transaction.get_dataset(dataset_id=dataset_id, db=db)
    if not dataset:
        raise exceptions.DatasetDoesNotExist()
    if dataset.status != DatasetState.COMPLETED:
        return schemas.FileResponse(
            success=False,
            dataset_status=dataset.status,
            error_message=dataset.error_message,
        )
    companies_data = transaction.get_companies(dataset_id=dataset_id, db=db)
    companies_data_dict = [i.__dict__ for i in companies_data]
    df = pd.DataFrame.from_records(companies_data_dict)
    df = df.drop(columns=["_sa_instance_state"])
    file_path = f"temp_files/{dataset.id}.csv"
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    file_extension = get_file_extension(filename=dataset.dataset_name)
    file_name = dataset.dataset_name.rstrip(file_extension) + ".csv"
    return schemas.FileResponse(
        success=True,
        dataset_status=dataset.status,
        error_message=dataset.error_message,
        file_path=file_path,
        file_name=file_name,
    )
