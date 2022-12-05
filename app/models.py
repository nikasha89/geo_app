"""SQLAlchemy Data Models."""
import json

from fastapi.logger import logger
from geoalchemy2 import Geometry
from sqlalchemy import Column, UniqueConstraint, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, Float

from .config import settings
from .db import get_srid

Base = declarative_base(MetaData())
engine = create_engine(settings.db_url, echo=True)


class PayStat(Base):
    __tablename__ = "paystats"
    __table_args__ = (UniqueConstraint('postal_code', 'age', 'gender', 'month', 'year', name='pay_stat_constraint_1'),
                      {'extend_existing': True})

    id = Column(Integer, primary_key=True, unique=True, autoincrement="auto")
    postal_code = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Text, nullable=False)
    total_amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    def __init__(self, session, postal_code, age, gender, total_amount, month, year):
        self.postal_code = postal_code
        self.age = age
        self.gender = gender
        self.total_amount = total_amount
        self.month = month
        self.year = year
        session.add(self)
        session.commit()
        logger.info(f"{self.__repr__()} was inserted into {self.__tablename__}.")

    def __iter__(self):
        yield from {
            "postal_code": self.postal_code,
            "age": self.age,
            "gender": self.gender,
            "total_amount": self.total_amount,
            "month": self.month,
            "year": self.year,
        }.items()

    def __repr__(self):
        return f"<Date = {self.month}/{self.year}; Postal Code = {self.postal_code}; " \
               f"Age = {self.age}; Gender = {self.gender}; Total Amount = {self.total_amount} > "

    @staticmethod
    def save_dataframe(df):
        df.to_sql(
            'paystats',
            engine,
            if_exists='replace',
            index=True,
            index_label='id',
            dtype={
                "id": Integer,
                "postal_code": Integer,
                "age": Integer,
                "gender": Text,
                "total_amount": Float,
                "month": Integer,
                "year": Integer
            }
        )
        logger.info("Pay Stats data were inserted into postal codes table.")


class PostalCode(Base):
    __tablename__ = "postal_codes"
    __table_args__ = (UniqueConstraint('geom', name='postal_code_constraint_1'), {'extend_existing': True})

    id = Column(Integer, primary_key=True, unique=True, autoincrement="auto")
    postal_code = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    geom = Column(Geometry('POINT'), nullable=False)

    def __init__(self, session, postal_code, description, geometry):
        self.postal_code = postal_code
        self.description = description
        self.geom = geometry
        session.add(self)
        session.commit()
        logger.info(f"{self.__repr__()} was inserted into {self.__tablename__}.")

    def __iter__(self):
        yield from {
            "postal_code": self.postal_code,
            "description": self.description,
            "geometry": self.geom
        }.items()

    def __repr__(self):
        return f"<Postal Code = {self.postal_code}; geometry = {self.geom}>"

    @staticmethod
    def to_json(rows):
        data_json = []
        for row in rows:
            data = {
                'postal_code': row.postal_code,
                'description': row.description,
                "geo_json": json.loads(row.geo_json)
            }
            data_json.append(data)

        return data_json

    @staticmethod
    def save_dataframe(df):
        df.to_sql(
            'postal_codes',
            engine,
            if_exists='replace',
            index=True,
            index_label='id',
            dtype={
                "id": Integer,
                "postal_code": Integer,
                "description": Text,
                "geom": Geometry(geometry_type='POINT', srid=get_srid())
            }
        )
        logger.info("Postal Codes data were inserted into postal codes table.")


Base.metadata.create_all(engine)
