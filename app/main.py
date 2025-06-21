import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.constants import (
    APP_VERSION,
    CONTACT,
    DESCRIPTION,
    LICENSE,
    SWAGGER_FAVICON_URL,
    SWAGGER_UI_PARAMETERS,
    TITLE,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=TITLE,
    version=APP_VERSION,
    description=DESCRIPTION,
    contact=CONTACT,
    license_info=LICENSE,
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
    swagger_favicon_url=SWAGGER_FAVICON_URL,
)


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")
