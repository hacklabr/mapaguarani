#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py migrate

/usr/local/bin/gunicorn wsgi -t 1200 -w 4 -b 0.0.0.0:5000 --chdir=/app/mapaguarani \
    --error-logfile=- \
    --access-logfile=- \
    --log-level info
