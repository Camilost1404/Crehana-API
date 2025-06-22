import logging
import time

from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse

from app.core.api import api_router
from app.core.constants import (
    APP_VERSION,
    CONTACT,
    DESCRIPTION,
    LICENSE,
    SWAGGER_FAVICON_URL,
    SWAGGER_UI_PARAMETERS,
    TITLE,
)
from app.core.database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Database Initialization...")
    try:
        init_db()
        logger.info("Database Initialization Complete.")
        yield
    finally:
        logger.info("Application shutdown...")


app = FastAPI(
    title=TITLE,
    version=APP_VERSION,
    description=DESCRIPTION,
    contact=CONTACT,
    license_info=LICENSE,
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
    swagger_favicon_url=SWAGGER_FAVICON_URL,
    lifespan=lifespan,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router)


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")
