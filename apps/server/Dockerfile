# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /server

# Install PostgreSQL development libraries, PostgreSQL client utilities, and other dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the wait-for-it and entrypoint scripts
COPY wait-for-it.sh /wait-for-it.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /wait-for-it.sh /entrypoint.sh

# Copy the requirements file into the image
COPY requirements.txt /server/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /server/

# Collect static files
RUN python manage.py collectstatic --noinput

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Expose port 8000
EXPOSE 8000
