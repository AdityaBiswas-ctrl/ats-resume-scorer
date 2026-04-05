# Dockerfile

# Use an official Python slim image — smaller and faster than the full image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer, so it won't reinstall
# packages every time you change your code (only when requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy model during build time, not at runtime
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY app/ ./app/

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]