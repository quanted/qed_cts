#!/bin/bash
django-admin.py collectstatic --noinput 
cd /src && daphne -b 0.0.0.0 -p 8000 asgi_docker:channel_layer