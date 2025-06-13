#!/bin/bash
python manage.py runserver_plus --cert-file dev.crt --key-file dev.key 127.0.0.1:8000
