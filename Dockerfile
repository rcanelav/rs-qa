FROM python:3.10-slim AS base

WORKDIR /app

# Install build dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

# Copy application files
COPY requirements.txt pyproject.toml uv.lock .python-version ./
COPY ./src ./src

# Install Python dependencies from requirements.txt
RUN uv pip install --system -r requirements.txt

# Expose the app port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]