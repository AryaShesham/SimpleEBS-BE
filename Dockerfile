# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Install additional packages for Celery and Redis
RUN pip install --no-cache-dir celery redis

# Expose the port(s) you need
EXPOSE 8000

# Set up Celery worker command (you can adjust this as needed)
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    celery -A project_ebs worker --loglevel=info
