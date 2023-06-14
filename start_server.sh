#!/usr/bin/env bash
# This script starts ecity web server with gunicorn production server instead
# of the flask web server

# pip install gunicorn
sudo gunicorn --bind 0.0.0.0:5000 ecity.app.ecity_app:app
