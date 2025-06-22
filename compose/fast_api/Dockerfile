# Etapa base
FROM python:3.12-slim as builder

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.1 \
    PATH="/root/.local/bin:$PATH" \
    APP_HOME=/app

# Instalar dependencias para construir paquetes de Python
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    vim \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION \
    && poetry config virtualenvs.create false

# Directorio de trabajo
WORKDIR ${APP_HOME}

# Copiar archivos de configuración de Poetry
COPY ./poetry.lock ./pyproject.toml ./

# Instalar dependencias principales
RUN poetry install --only main

# Etapa de runtime
FROM python:3.12-slim as runner

ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    FASTAPI_ENV=development

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar paquetes instalados de la etapa de build
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar script de arranque
COPY ./compose/fast_api/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./compose/fast_api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copiar el resto de la app
WORKDIR ${APP_HOME}
COPY . .

EXPOSE 8000
ENTRYPOINT [ "/entrypoint.sh" ]
