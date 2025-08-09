ACTIVATE_BASH=source ~/.bashrc
ACTIVATE_VENV= poetry shell
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/ cache/ config/
DIR_NO_TESTS = app/ controllers/ data/ scripts/ utils/ cache/
SERVICES = db db_backup redis rabbitmq api mongo worker cassandradb scylladb surrealdb minio
AIRFLOW_SERVICES = airflow-webserver airflow-scheduler airflow-worker airflow-triggerer airflow-init airflow-cli flower
SPARK_SERVICES = spark-master spark-worker
KAFKA_SERVICES = zookeeper broker
ELK_SERVICES = elasticsearch logstash kibana setup
NIFI_SERVICES = nifi rabbitmq minio zookeeper broker
DOCKER_COMPOSES = -f docker-compose.yml -f docker-compose-airflow.yml -f docker-compose-spark.yml -f docker-compose-kafka.yml -f docker-compose-elk.yml -f docker-compose-nifi.yml
FULL_SERVICES = $(SERVICES) $(AIRFLOW_SERVICES) $(SPARK_SERVICES) $(KAFKA_SERVICES) $(ELK_SERVICES)
BASIC_SERVICES = $(SERVICES) $(ELK_SERVICES)
USER=$(shell whoami)
# for mac os install coreutils ot get nproc
CORES := $(sysctl -n hw.ncpu)
MANUAL_CORES=8


venv_create:
	pip install poetry
	poetry install --no-root
	poetry run pre-commit install
	apt update && apt install -y default-jre

venv_update:
	poetry update
	poetry self add poetry-plugin-up
	poetry up

venv_delete:
	poetry env remove --all

typehint:
	poetry run mypy $(DIR_ARGS)

lint:
	poetry run ruff check $(DIR_ARGS)

format:
	poetry run ruff format $(DIR_ARGS)

test_parallel:
	poetry run  pytest -n $(MANUAL_CORES) --timeout=20 tests/ -W ignore::DeprecationWarning

test:
	poetry run  pytest --timeout=20 tests/ -W ignore::DeprecationWarning

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

basic:
	docker compose --env-file $(ENV_FILE)  $(DOCKER_COMPOSES) up -d --build $(BASIC_SERVICES)

elk:
	docker compose --env-file $(ENV_FILE)  $(DOCKER_COMPOSES)  up -d $(ELK_SERVICES)

nifi:
	docker compose --env-file $(ENV_FILE)  $(DOCKER_COMPOSES)  up -d $(NIFI_SERVICES)

kafka:
	docker compose --env-file $(ENV_FILE)  $(DOCKER_COMPOSES)  up -d $(KAFKA_SERVICES)

start_services:
	docker compose --env-file $(ENV_FILE) up -d $(SERVICES)

start:
	docker compose --env-file $(ENV_FILE) $(DOCKER_COMPOSES) up -d  $(FULL_SERVICES)

build:
	docker compose --env-file $(ENV_FILE) $(DOCKER_COMPOSES) build $(FULL_SERVICES)

update:
	docker compose --env-file $(ENV_FILE) $(DOCKER_COMPOSES) pull
	make start

stop:
	docker stop $$(docker ps -a -q)
	docker rm $$(docker ps -a -q)
	make remove_volumes

clean:
	make stop
	make remove_images
	docker system prune -af

remove_images:
	docker rmi $$(docker images -aq)

remove_volumes:
	docker volume rm $$(docker volume ls -q)

start_celery_workers:
	poetry run celery -A celery_worker worker --loglevel=info

start_celery_workers_detached:
	poetry run celery -A celery_worker worker --loglevel=info --detach


bare_bones: venv_create start_services test_parallel sr_services

soft_checklist: typehint coverage lint
hard_checklist: format lint typehint test coverage
