FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy all necessary files for package installation
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# Install dependencies and the package
RUN uv sync --frozen --no-dev

# Copy database
COPY chinook.db ./

EXPOSE 5002

CMD ["uv", "run", "python", "-m", "chinook_service", "--host", "0.0.0.0", "--port", "5002"]
