# Use official Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip-tools first
RUN pip install --upgrade pip && pip install pip-tools

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies from the compiled requirements.txt
RUN pip install -r requirements.txt

# Copy Django project files
COPY . .

RUN python manage.py collectstatic --noinput

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start the server
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]