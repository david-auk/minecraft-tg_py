# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install necessary utilities
RUN apt-get update && apt-get install -y wget

RUN wget https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.deb && \
    dpkg -i jdk-21_linux-x64_bin.deb || true

# Set JAVA_HOME
ENV JAVA_HOME="/usr/lib/jvm/java-21-oracle-x64"
ENV PATH="$PATH:$JAVA_HOME/bin"

# Copy the current directory contents into the container at /app
COPY ./requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Get the port for flask to run on
ARG FLASK_PORT

# Get and create the server root dir
ARG MINECRAFT_SERVER_ROOT
RUN mkdir -p "$MINECRAFT_SERVER_ROOT"

# Make the flask port available to the world outside this container
EXPOSE ${FLASK_PORT}

# Create new user
RUN useradd -ms /bin/bash nonrootuser

# Make the new user have read/write permissions within the server root dir
RUN chown nonrootuser:nonrootuser "$MINECRAFT_SERVER_ROOT"

# Demote to non root lever
#USER nonrootuser

# Define environment variable
ENV PYTHONPATH="/app"
ENV FLASK_APP=app/flask/app.py
ENV FLASK_RUN_PORT=${FLASK_PORT}
ENV FLASK_RUN_HOST=0.0.0.0
ENV MINECRAFT_SERVER_ROOT=${MINECRAFT_SERVER_ROOT}

# Run the application
#CMD ["waitress-serve", "--port=5050", "--call", "app:create_app"]
#CMD ["flask", "run"]
CMD ["python", "-m", "app.flask.app"]
