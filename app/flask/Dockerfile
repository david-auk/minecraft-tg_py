# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Get the port for flask to run on
ARG FLASK_PORT

# Make the flask port available to the world outside this container
EXPOSE ${FLASK_PORT}

RUN useradd -ms /bin/bash nonrootuser

# Demote to non root lever
USER nonrootuser

# Define environment variable
ENV FLASK_APP=flask/app.py
ENV FLASK_RUN_PORT=${FLASK_PORT}
ENV FLASK_RUN_HOST=0.0.0.0
# Run the application
#CMD ["waitress-serve", "--port=5050", "--call", "app:create_app"]
CMD ["flask", "run"]