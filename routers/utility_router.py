import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from models.shared.shared_models import PrettyJSONResponse


router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Sets up compact logging, for all API requests.
    """
    logger = logging.getLogger('uvicorn.access')
    handler = logging.handlers.RotatingFileHandler('logs/api_short.log', mode='a', maxBytes=100*1024, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    yield


@router.get('/status', status_code=200, response_class=PrettyJSONResponse)
def api_status():
    """
    Utility route for testing api functionality.
    """
    return {'message': 'Schedule shows productions API is up and running!'}
