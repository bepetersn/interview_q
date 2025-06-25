#! /usr/bin/env bash

# Collect environment variables from Elastic Beanstalk
set -a
source /opt/elasticbeanstalk/deployment/env
set +a

source $PYTHONPATH/activate
psql -U postgres -c "create database $RDS_DB_NAME;"
python manage.py migrate
