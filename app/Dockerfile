FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# The code imports `app.etl` and the root-level `config`, so both sit under /app.
COPY config.py ./
COPY app ./app

# CREDS_PATH: the token cache now lives under /app/app/etl with the rest of the code.
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH=/app CREDS_PATH=/app/app/etl/.creds

ENTRYPOINT ["./app/docker_entrypoint.sh"]
