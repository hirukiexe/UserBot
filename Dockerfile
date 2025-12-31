# Base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Dependencies copy (agar requirements.txt ho)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# App files copy
COPY . .

# Run main.py
CMD ["python", "main.py"]
