# Build file for django with channels using asgi server daphne

FROM puruckertom/qed_py27

# Copy the project code
COPY . /src/

WORKDIR /src

RUN useradd --system app
RUN chown app:app /src

# Install Python Dependencies
RUN pip install --requirement /src/requirements.txt

USER app

# Specific Docker-specific Django settings file (needed for collectstatic)
ENV DJANGO_SETTINGS_MODULE="settings_docker"

# Add project root to PYTHONPATH (needed to import custom Django settings)
ENV PYTHONPATH="/src"