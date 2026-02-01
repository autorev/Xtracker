# Python image
FROM python:3.11-slim

# Prevents Python from buffering stdout/stderr (crucial for real-time logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

CMD ["python", "main.py"]