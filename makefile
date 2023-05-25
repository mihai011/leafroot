ACTIVATE_BASH=source ~/.bashrc
ACTIVATE_VENV= poetry shell
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/ cache/ config/
DIR_NO_TESTS = app/ controllers/ data/ scripts/ utils/ cache/
SERVICES = db redis rabbitmq api mongo worker cassandra scylladb
AIRFLOW_SERVICES = airflow-webserver airflow-scheduler airflow-worker airflow-triggerer airflow-init airflow-cli flower
FULL_SERVICES = $(SERVICES) pgadmin $(AIRFLOW_SERVICES)
USER=$(shell whoami)
# for mac os install coreutils ot get nproc
CORES := $(shell nproc)
MANUAL_CORES=8


venv_create:
	poetry install
	poetry run pre-commit install

venv_update:
	poetry update

typehint:
	poetry run mypy $(DIR_ARGS)

lint:
	poetry run pylint $(DIR_ARGS)

format:
	poetry run black $(DIR_ARGS)

test_parallel:
	poetry run  pytest -n $(MANUAL_CORES) tests/ -W ignore::DeprecationWarning

test:
	poetry run  pytest tests/ -W ignore::DeprecationWarning

coverage:
	poetry run pytest --cov-report term-missing --cov=. --cov-report html tests/

coverage_parallel:
	poetry run  pytest --cov-report term-missing --cov=. -n $(MANUAL_CORES) tests/

start_production:
	poetry run  gunicorn app.app:app --workers $(CORES) --preload -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:$(PORT)

start_development:
	poetry run  uvicorn app.app:app --host 0.0.0.0 --port $(PORT) --reload

start_development_docker:
	poetry run  alembic upgrade head
	poetry run  uvicorn app.app:app --host 0.0.0.0 --port $(PORT) --reload

start_production_docker:
	poetry run  alembic upgrade head
	make start_production

# make sure to login to ngrok so it can server html responses
make ngrok:
	ngrok http $(PORT)

bandit:
	poetry run bandit -c pyproject.toml -r $(DIR_NO_TESTS)

pydocstyle:
	poetry run pydocstyle  $(DIR_ARGS)

doc8:
	poetry run doc8 $(DIR_ARGS)

docformatter:
	poetry run docformatter --in-place -r $(DIR_ARGS)

pycodestyle:
	poetry run pycodestyle -r $(DIR_ARGS)

start_services:
	docker compose --env-file $(ENV_FILE) up -d $(SERVICES)

start_full_services:
	docker compose --env-file $(ENV_FILE) -f docker-compose.yml -f docker-compose-airflow.yml up -d $(FULL_SERVICES)

stop_services:
	docker compose --env-file $(ENV_FILE) stop $(SERVICES)

sr_services:
	docker compose --env-file $(ENV_FILE) down

build:
	docker build -t test --target prod -f

docker_update:
	docker compose --env-file $(ENV_FILE) pull
	make start_full_services

remove_images:
	docker rmi $$(docker images -aq)

docker_stop:
	docker stop $$(docker ps -a -q)
	docker rm $$(docker ps -a -q)

docker_clean:
	make docker_stop
	make remove_images
	docker volume rm $$(docker volume ls -q)


start_celery_workers:
	poetry run celery -A celery_worker worker --loglevel=info

start_celery_workers_detached:
	poetry run celery -A celery_worker worker --loglevel=info --detach


bare_bones: venv_create start_services test_parallel sr_services

soft_checklist: typehint coverage lint
hard_checklist: format lint typehint test coverage
