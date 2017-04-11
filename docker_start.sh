#!/bin/bash

django-admin.py collectstatic --noinput       # "Collect" static files (--noinput executes the command w/o user interaction)
# exec uwsgi /etc/uwsgi/uwsgi.ini               # Start uWSGI (HTTP router that binds Python WSGI to a web server, e.g. NGINX)
# python manage.py runserver --noworker
# from https://channels.readthedocs.io/en/stable/deploying.html
# daphne my_project.asgi:channel_layer
# daphne asgi_docker:channel_layer  # use asgi_docker.py, channel_layer
# cd /src && exec daphne -b 0.0.0.0 -p 8000 asgi_docker:channel_layer
daphne -b 0.0.0.0 -p 8080 asgi_docker:channel_layer