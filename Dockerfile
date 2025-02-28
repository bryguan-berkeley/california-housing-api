# Set Base Image
FROM python:3.12-slim AS builder

# Set Container's Working Directory
WORKDIR /app

    # Update Package List
RUN apt-get update && \
    # Install Packages
    apt-get install -y \
         curl \
         build-essential \
         libffi-dev && \
    # Delete Package List
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add Poetry Directory to Path
ENV PATH=/root/.local/bin:${PATH}
# Copy toml, lock from Local Current Directory to Container Current Directory
COPY pyproject.toml poetry.lock ./
# Create Virtual Environment in /app/venv Directory
RUN python -m venv /app/venv
# Activate Virtual Environment
RUN . /app/venv/bin/activate && \
    # Install Production Dependencies into Virtual Environment
    poetry install --only main --no-root

# Set Base Image
FROM python:3.12-slim AS runner 

# Set Container's Working Directory
WORKDIR /app
# Copy Virtual Environment from Builder to Runner
COPY --from=builder /app/venv /app/venv

# Copy src from Local Current Directory to Container Current Directory
COPY src/ ./src/
# Copy model_pipeline.pkl from Local Current Directory to Container Current Directory
COPY model.pkl ./
# Add Virtual Environment Directory w/ Poetry Dependencies to Path
ENV PATH=/app/venv/bin:${PATH}

# Launch w/ Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]