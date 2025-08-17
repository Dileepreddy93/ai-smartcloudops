# Simple Docker image for the Flask dashboard

FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY src ./src
COPY data ./data

EXPOSE 5000

CMD ["python", "src/dashboard.py"]


