#!/bin/bash
python manage.py runserver_plus --cert-file localhost.pem --key-file localhost-key.pem 0.0.0.0:8000
