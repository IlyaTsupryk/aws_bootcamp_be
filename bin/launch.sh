#!/bin/bash

gunicorn --bind :8080 --workers 2 gallery/wsgi.py