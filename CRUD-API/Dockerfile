## Build Stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies within the virtual environment
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install Flask pymongo

## Runtime Stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

# Explicitly copy the app.py file
COPY app.py /app/

# Expose port
EXPOSE 8000

# Set the virtual environment path
ENV PATH="/app/venv/bin:$PATH"

# Run the application
CMD ["python3", "app.py"]
