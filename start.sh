#!/bin/bash

exec gunicorn_django -c ../gunicorn.conf.py


