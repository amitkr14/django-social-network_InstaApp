# Pull modern official base image
FROM python:3.11-slim-bookworm

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "socialproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]