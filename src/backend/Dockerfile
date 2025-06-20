FROM python:3.13-slim@sha256:d97b595c5f4ac718102e5a5a91adaf04b22e852961a698411637c718d45867c8

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
LABEL org.opencontainers.image.source=https://github.com/sebastiantress03/Projekt-Software-Engineering
CMD ["fastapi", "run", "backend.py", "--host", "0.0.0.0", "--port", "8000"]