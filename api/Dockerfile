FROM python:3.13-alpine

RUN adduser --disabled-password --gecos '' python;\
    mkdir /opt/python;\
    chown python:python /opt/python


USER python
WORKDIR /opt/python
RUN ["mkdir", "-p", "data"]

COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /uvx /bin/

# Show messages on the console
ENV PYTHONUNBUFFERED=1

ENV PATH="/home/python/.local/bin:/opt/python/.venv/bin:/root/.local/bin:$PATH"

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the project into the image
COPY --chown=python:python . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
