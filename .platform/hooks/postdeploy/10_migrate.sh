#!/usr/bin/env bash

set -e
source /var/app/venv/*/bin/activate
python manage.py migrate --noinput
