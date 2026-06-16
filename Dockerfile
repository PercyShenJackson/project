# --- Stage 1: Build dependencies ---
# --- Stage 1: Build dependencies ---
FROM python:3.14-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install build dependencies if your packages need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a local directory
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final lightweight runtime ---
FROM python:3.14-slim AS runner

WORKDIR /app

ENV PYTHONTONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /root/.local /root/.local

# Copy everything from your local directory into the container's /app directory
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 3000

# UPDATE THIS: Change "main.py" to whatever your main Python file is called
CMD ["python", "app.py"]
