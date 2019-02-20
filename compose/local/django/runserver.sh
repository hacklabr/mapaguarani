#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

npm install

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py runserver_plus 0.0.0.0:8000
