#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Start the FastAPI server using uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
