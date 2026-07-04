FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . ./backend

# Set python path to allow imports from root /app directory
ENV PYTHONPATH=/app
ENV PORT=8080
EXPOSE 8080

# Run the FastAPI server module
CMD ["python", "-m", "backend.main"]
