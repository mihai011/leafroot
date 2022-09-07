ACTIVATE_BASH=source ~/.bashrc
ACTIVATE_VENV=. venv/bin/activate
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/ cache/ config/
DIR_NO_TESTS = app/ controllers/ data/ scripts/ utils/ cache/
SERVICES = celery_worker db redis rabbitmq phppgadmin

CORES=`nproc`
MANUAL_CORES=8

ENV_FILE_DEV=config/config_files/.env_dev
ENV_FILE_PROD=config/config_files/.env_prod
ENV_FILE_USER=.env_user

venv_create: venv_delete stable_packages_versions.txt
	python3 -m venv venv
	$(ACTIVATE_VENV) && pip install --upgrade pip
	$(ACTIVATE_VENV) && pip install --no-cache-dir -r requirements.txt
	$(ACTIVATE_VENV) && pip freeze > stable_packages_versions.txt
	$(ACTIVATE_VENV) && pre-commit install

venv_delete:
	rm -rf venv/

venv_update: venv_delete
	make venv_create

typehint:
	$(ACTIVATE_VENV) && mypy $(DIR_ARGS)

test_parallel: start_celery_worker
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest -n $(MANUAL_CORES) tests/
	make stop_celery_worker

test: start_celery_worker
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest tests/
	make stop_celery_worker

lint:
	$(ACTIVATE_VENV) && pylint $(DIR_ARGS)

format:
	$(ACTIVATE_VENV) && black $(DIR_ARGS)

coverage: start_celery_worker
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest --cov-report term-missing --cov=.  tests/
	make stop_celery_worker

coverage_parallel: start_celery_worker
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest --cov-report term-missing --cov=. -n $(MANUAL_CORES) tests/
	make stop_celery_worker

start_production: venv_create
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_PROD) gunicorn app.app:app --workers $(CORES) -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0

start_development:
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) uvicorn app.app:app --host 0.0.0.0 --reload

start_celery_worker:
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) celery -A celery_worker worker --loglevel=info --detach

stop_celery_worker:
	$(ACTIVATE_VENV) && python3 scripts/stop_celery_workers.py

start_db:
	docker-compose up -d db

bandit:
	$(ACTIVATE_VENV) && bandit -c pyproject.toml -r $(DIR_NO_TESTS)

pydocstyle:
	$(ACTIVATE_VENV) && pydocstyle  $(DIR_ARGS)

doc8:
	$(ACTIVATE_VENV) && doc8 $(DIR_ARGS)

docformatter:
	$(ACTIVATE_VENV) && docformatter --in-place -r $(DIR_ARGS)

pycodestyle:
	$(ACTIVATE_VENV) && pycodestyle -r $(DIR_ARGS)

start_services:
	docker-compose --env-file $(ENV_FILE_USER) up -d $(SERVICES)

stop_services:
	docker-compose --env-file $(ENV_FILE_USER) stop

sr_services:
	docker-compose stop $(SERVICES)
	docker-compose rm -f $(SERVICES)

docker_clean:
	docker system prune -af

docker_update:
	docker-compose pull
	make start_services

env_file:
	cp config/config_files/.env_dev $(ENV_FILE_USER)

bare_bones: env_file venv_create start_services test_parallel sr_services

soft_checklist: typehint coverage lint
hard_checklist: format lint typehint test coverage

install_rust:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y

rust_workers:
	$(ACTIVATE_VENV) && cd celery_rust_workers && maturin develop
