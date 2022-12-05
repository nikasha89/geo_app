# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.db import Database, get_srid
from app.models import PostalCode, PayStat
from sqlalchemy import func
from fastapi.logger import logger
import logging
from app.serialization.stats_geometry import StatsGeometry
from app.serialization.stats_geometry_group_by_cp import StatsGeometryGroupByCp

title_app = "GeoAPP - API"
description_app = "API - GeoAPP - GIS"
version_app = "3.8.0"
app = FastAPI(title=title_app,
              description=description_app,
              version=version_app,
              docs_url="/docs",
              redoc_url="/redoc",
              terms_of_service="https://gist.github.com/efernandezleon/ce1e07036d85775756cdaaa8289c5191",
              contact={
                  "name": "Ana Rodríguez González",
                  "url": "https://www.linkedin.com/in/anarodgon/?locale=en_US",
                  "email": "nikasha89@gmail.com",
              },
              license_info={
                  "name": "Copyright 2022",
                  "path": "./resources/LICENSE",
              })
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
database = Database()


@app.get("/")
def get_root():
    return "Welcome  to API - GIS - GeoApp!"


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

    database.load_files_into_db()
    # create a dummy entry
    # PayStat(database.session, 23899, 12, "P", 258.98, 12, 2022)
    # PostalCode(database.session, 41620, 43.24, 1.532)
    # PostalCode(database.session, 41620, -42.3658, 65.2289)
    # PostalCode(database.session, 41610, 2.3658, -25.7563)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/postal_code/{postal_code}")
def get_postal_code(postal_code: int):
    rows = database.session.query(PostalCode.postal_code, PostalCode.description,
                                  func.ST_AsGeoJSON(func.ST_Transform(PostalCode.geom, get_srid())).label("geo_json")) \
        .filter(PostalCode.postal_code == postal_code).all()

    return PostalCode.to_json(rows)


@app.get("/postal_codes")
def get_postal_codes():
    rows = database.session.query(PostalCode.postal_code, PostalCode.description,
                                  func.ST_AsGeoJSON(func.ST_Transform(PostalCode.geom, get_srid())).label("geo_json")) \
        .all()
    return PostalCode.to_json(rows)


@app.get("/paystats")
def get_paystats():
    result = database.session.query(PayStat).all()

    return result


@app.get("/stats_geometry")
def get_stats_geometry():
    rows = database.session.query(PostalCode.postal_code, PostalCode.description,
                                  func.ST_AsGeoJSON(func.ST_Transform(PostalCode.geom, get_srid())).label("geo_json"),
                                  PayStat.age, PayStat.gender, PayStat.total_amount, PayStat.month, PayStat.year) \
        .join(PayStat, PayStat.postal_code == PostalCode.postal_code).all()

    return StatsGeometry.stats_geometry_to_json(rows)


@app.get("/stats_geometry_group_by_cp")
def stats_geometry_group_by_cp():
    rows = database.session.query(PostalCode.postal_code, PostalCode.description,
                                  func.ST_AsGeoJSON(func.ST_Transform(PostalCode.geom, get_srid())).label("geo_json"),
                                  PayStat.age, PayStat.gender, PayStat.total_amount, PayStat.month, PayStat.year) \
        .join(PayStat, PayStat.postal_code == PostalCode.postal_code).all()

    stats_geometry_group_by_cp_object = StatsGeometryGroupByCp.get_stats_geometry_group_by_cp(rows)

    return StatsGeometryGroupByCp.stats_geometry_group_by_cp_to_json(stats_geometry_group_by_cp_object)


def custom_openapi():
    openapi_schema = get_openapi(
        title=title_app,
        version=version_app,
        description=description_app,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "path": "./resources/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
