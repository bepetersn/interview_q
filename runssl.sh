#!/bin/bash
python manage.py runserver_plus --cert-file example.com+5.pem --key-file example.com+5-key.pem 127.0.0.1:8000
