## ----------------------------------------------------------------------
## Script for useful command execution and memorization
## ----------------------------------------------------------------------

include .env

DC = docker compose -f compose.yaml
PY = $(DC) exec backend

help:		## Use one of below commands
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

## ----------------------------------------------------------------------
## DOCKER CONTAINERS MANAGEMENT
## ----------------------------------------------------------------------

watch:		## Run docker compose with watch
	$(DC) up --watch
up:		## Start docker compose up
	$(DC) up --remove-orphans
buildup:	## Run docker compose up with build flag
	$(DC) up --build --remove-orphans
down:		## Run docker compose down
	$(DC) down
down-v:		## Run docker compose down + volumes
	$(DC) down -v
logs:		## Show docker logs
	$(DC) logs
prune:		## Prune all docker images + volumes
	docker system prune -a --volumes

## ----------------------------------------------------------------------
## BACKEND CONTAINER COMMANDS
## ----------------------------------------------------------------------

be-shell:	## Execute backend container shell
	$(PY) sh
be-updates:	## Check if new dependencies updates are available
	$(PY) uv lock --check
be-restart:	## Restart backend container
	$(DC) restart backend
be-run-shell:	## start backend container and run shell
	$(DC) run backend sh

## ----------------------------------------------------------------------
## BACKEND COMMANDS
## ----------------------------------------------------------------------

lint-check:	## Lint backend code
	$(PY) uv run ruff check --fix
format-code:	## Format backend code
	$(PY) uv run ruff format
req-gen:	## Generate requirements.txt file
	uv export --frozen --format requirements-txt --directory ./api -o requirements.txt

venv-create:	## Create project virtual environment
	uv venv ./api/.venv
	uv sync --frozen --directory ./api
