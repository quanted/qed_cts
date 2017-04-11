# Hosts django project w/ uwsgi

#FROM python:2.7
FROM puruckertom/qed_py27

# Install Python Dependencies
# COPY requirements.txt /tmp/
COPY . /src/
RUN pip install --requirement /src/requirements.txt

# Install uWSGI
RUN pip install uwsgi

# Overwrite the uWSGI config
COPY uwsgi.ini /etc/uwsgi/

WORKDIR /src
EXPOSE 8080

# Ensure "docker_start" is executable
RUN chmod 755 /src/docker_start.sh

# Specific Docker-specific Django settings file (needed for collectstatic)
ENV DJANGO_SETTINGS_MODULE="settings_docker"

# Add project root to PYTHONPATH (needed to import custom Django settings)
ENV PYTHONPATH="/src"

CMD ["sh", "/src/docker_start.sh"]