# app/db.py
"""Database engine & session creation."""
import os
import pathlib
import pandas as pd
import geopandas as gpd
from geoalchemy2 import WKTElement
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.logger import logger
from .config import settings, get_srid
from .models import PostalCode, PayStat
from shapely import wkt


def read_file(path):
    df = pd.read_csv(path)
    df.crs = f"epsg:{get_srid()}"

    return df


class Database:
    is_connected = False
    session = None
    engine = create_engine(settings.db_url, echo=True)
    metadata = MetaData(engine)
    Base = declarative_base(metadata)

    def __init__(self):
        self.logger = logger
        self.connect()

    def connect(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.is_connected = True
        logger.info("Connected to DB.")

    def disconnect(self):
        self.session.close()
        logger.info("Disconnected from DB.")

    def load_files_into_db(self):
        if not self.is_connected:
            self.connect()

        df_pay_stats = read_file(os.path.join(pathlib.Path(__file__).parent.resolve(), 'db_files/paystats.csv'))
        gdf_postal_codes = read_file(os.path.join(pathlib.Path(__file__).parent.resolve(), 'db_files/postal_codes.csv'))

        gdf_postal_codes['geometry'] = gdf_postal_codes['geometry'].apply(wkt.loads)
        gdf_postal_codes = gpd.GeoDataFrame(gdf_postal_codes, crs=gdf_postal_codes.crs)
        gdf_postal_codes['geom'] = gdf_postal_codes['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
        gdf_postal_codes.drop('geometry', 1, inplace=True)

        PayStat.save_dataframe(df_pay_stats)
        PostalCode.save_dataframe(gdf_postal_codes)

        logger.info("Data from files was loaded.")
