#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ -z "${POSTGRES_USER}" ]; then
    POSTGRES_DEFAULT_USER="postgres"
    export POSTGRES_USER="${POSTGRES_DEFAULT_USER}"
fi
# Constructing the PostgreSQL database URL
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

python << END
import sys
import time

import psycopg2
from psycopg2 import OperationalError

suggest_unrecoverable_after = 30
start = time.time()

while True:
    try:
        conn = psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
        conn.close()  # Close the connection if successful
        break
    except OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available...\n")

        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write(f"  This is taking longer than expected. The following exception may be indicative of an unrecoverable error: '{error}'\n")

    time.sleep(1)
END

>&2 echo 'PostgreSQL is available'

exec "$@"
