from . import Base

from sqlalchemy import Column, Integer, String, ForeignKey


class Datasets(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String)
    status = Column(String)


class Companies(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    linkedin_url = Column(String)
    employee_count = Column(Integer)