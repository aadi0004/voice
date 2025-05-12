# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    libportaudio2 \
    portaudio19-dev \
    espeak \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY .env .

# Expose Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]