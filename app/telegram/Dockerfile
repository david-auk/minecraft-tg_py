# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
#WORKDIR /app

# Copy the current directory contents into the container
COPY ./requirements.txt requirements.txt

# Set path so packages can be imported correctly
ENV PYTHONPATH="/app"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "-m", "app.telegram.main"]
#CMD ["sleep", "300"]