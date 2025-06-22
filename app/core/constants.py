from app.core.settings import settings

APP_NAME = settings.app_name
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
TITLE = "Crehana API - Prueba Técnica"
APP_VERSION = settings.app_version
DESCRIPTION = """
Esta aplicación es una prueba técnica realizada según lo especificado,
mostrando una interfaz RESTful para acceder a contenido educativo, recursos y
herramientas diseñadas para estudiantes y educadores.
"""
CONTACT = {"name": "Andres Camilo Torres Rosales", "email": "camitorres1404@gmail.com"}
LICENSE = {"name": "MIT", "url": "https://opensource.org/license/mit/"}
SWAGGER_UI_PARAMETERS = {"syntaxHighlight.theme": "obsidian"}
SWAGGER_FAVICON_URL = "https://example.com/your-favicon.ico"
