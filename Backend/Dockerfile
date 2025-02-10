# Use a slimmer Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (and clean up apt cache)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove gcc

# Copy and install Python dependencies first (to take advantage of Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django application
COPY . .

# Expose the necessary port for the application
EXPOSE 8000



# Alternatively, use Django's runserver for development (uncomment for development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
