FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ ./src
COPY .github/core/ ./.github/core/

# Final sync to install the project
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

# For cloud deployment
# CMD ["alpaca-mcp-server", "serve", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "start.py"]