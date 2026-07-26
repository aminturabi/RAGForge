FROM python:3.10-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Hugging Face Spaces uses port 7860
EXPOSE 7860

# Run Flask via gunicorn listening on port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
