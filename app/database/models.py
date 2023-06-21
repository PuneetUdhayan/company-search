from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey

from . import Base


class DatasetState(Enum):
    PROCESSING = 1
    ERROR = 2
    COMPLETED = 3


class Datasets(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String)
    status = Column(Integer)
    error_message = Column(String)


class Companies(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    company = Column(String)
    linkedin_url = Column(String)
    employee_count = Column(Integer)
