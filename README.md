# FastAPI backend FoxAdventure cruise passengers

<center>

[![FastAPI](https://img.shields.io/badge/fastapi-%23009485.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![HTMX](https://img.shields.io/badge/HTMX-36C?logo=htmx&logoColor=fff)](https://htmx.org/)

[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-orange.svg)](https://docs.astral.sh/ruff/)
<a href="https://www.python.org/dev/peps/pep-0008/"><img alt="Code style: pep8" src="https://img.shields.io/badge/code%20style-pep8-orange.svg"></a>

</center>

Simple app for getting list of cruise ships data for Akureyri ports and tracking data updates to adjust passengers lists on booking systems.

## 1. Requirements

This development setup is tested in Linux environment. Overall components are deployed in Docker. It should work in Docker in Windows environment.

### Below software requirements are needed for the overall setup to work.

- **Docker:** container runtime environment
- **Docker Compose:** to package and manage multiple images together >=2.22 (for compose watch)
- **Python minimum version 3.13 and above**
- **make** (optional) - for simple commands execution
- **(UV)[https://docs.astral.sh/uv/guides/integration/docker/]** for creating virtual environment

## 2. Development instruction with Docker

First clone this directory and`cd` inside cloned directory.

Then create virtual environment with `make venv-create` command. Optionally you can use `uv venv` and `uv sync --frozen` commands inside `api` folder. `requirements.txt` file is also available inside `api` directory for other virtual environment tools.

Activate virtual environment to have all packages, libraries available for your editor:

```bash
source ./api/.venv/bin/activate
```

Create your `.env` from `.env.example` file and build docker image:

```bash
mv .env.example .env
```

Build and start the project by running:

```bash
make watch
```

App should run on `localhost:80` and should reload automatically. Thanks to `compose watch` container is automatically rebuild when changes are detected inside project libraries files `pyproject.toml` or `uv.lock`.

API Documentation:

- **SwaggerUI** API documentation is available under http://127.0.0.1:80/docs
- Alternative **ReDoc** documentation is under http://127.0.0.1:80/redoc

## 3. Deployment

TBD
