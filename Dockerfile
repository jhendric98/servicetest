FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/
COPY chinook.db ./

EXPOSE 5002

CMD ["uv", "run", "python", "-m", "chinook_service", "--host", "0.0.0.0", "--port", "5002"]
