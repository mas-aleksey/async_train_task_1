#!/usr/bin/env sh

gunicorn -c gunicorn_conf.py dj.wsgi:application
