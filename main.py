################################################################################
#       For API trial and documentation visit http://localhost:8000/docs       #
################################################################################
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger

from service.routes.utility_routes import lifespan
from persistence.sqlite_db import engine
from persistence.sql_alch_models import Base
from service.routes import crew, prod_crew, productions, utility_routes


def customize_openapi_schema():
    """
    Updates OpenAPI documentation details for SWAGGER UI.
    """
    openapi_schema = get_openapi(
        title='Manage Crew & Productions',
        version='2.8',
        summary='Crew management and show scheduling for production unit.',
        description=open('README.md', 'r').read(350),
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Start database
Base.metadata.create_all(bind=engine)

# Start API
app = FastAPI(lifespan=lifespan)

# Enable routes
app.include_router(utility_routes.router)
app.include_router(crew.router)
app.include_router(productions.router)
app.include_router(prod_crew.router)

# Manage detailed logging
log_abs_path = str(Path(__file__).resolve().parent) + '/logs/api_full.log'

logging.basicConfig(level=logging.INFO, filename=log_abs_path,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = add_custom_logger(app, disable_uvicorn_logging=False)

# Customize SWAGGER
app.openapi = customize_openapi_schema
