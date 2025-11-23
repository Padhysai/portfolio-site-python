FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for building some python packages)
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT:-5001}", "run:app"]
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-5001} run:app"]
