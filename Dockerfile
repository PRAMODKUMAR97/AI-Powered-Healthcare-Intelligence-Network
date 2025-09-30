# Use official Python image with version 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Add a constraints file to force compatible versions (especially for networkx)
COPY constraints.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && pip install --upgrade pip \
    && pip install -r requirements.txt -c constraints.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy entire project to the container
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set environment to avoid Streamlit asking for user input
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Streamlit entrypoint
CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
