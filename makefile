ACTIVATE_BASH=source ~/.bashrc
ACTIVATE_VENV=. venv/bin/activate
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/ cache/ config/
DIR_NO_TESTS = app/ controllers/ data/ scripts/ utils/ cache/
SERVICES = db redis rabbitmq pgadmin mongo
FULL_SERVICES = db redis rabbitmq pgadmin mongo backend
PORT=80
USER=$(shell whoami)
# for mac os install coreutils ot get nproc
CORES := $(shell nproc)
MANUAL_CORES=8

ENV_FILE_DEV=config/config_files/.env_dev
ENV_FILE_PROD=config/config_files/.env_prod
ENV_FILE_USER=.env_user

default: start_celery_workers

venv_create: venv_delete stable_packages_versions.txt
	pwd
	python3 -m venv venv
	$(ACTIVATE_VENV) && pip install --upgrade pip
	$(ACTIVATE_VENV) && pip install --no-cache-dir -r stable_packages_versions.txt
	$(ACTIVATE_VENV) && pre-commit install
	make rust_workers

venv_delete:
	rm -rf venv/

venv_update: venv_delete requirements.txt
	python3 -m venv venv
	$(ACTIVATE_VENV) && pip install --upgrade pip
	$(ACTIVATE_VENV) && pip install --no-cache-dir -r requirements.txt
	make rust_workers

stable_req:
	$(ACTIVATE_VENV) && pip freeze > stable_packages_versions.txt
	grep -v "celery_rust_workers" stable_packages_versions.txt > tmpfile && mv tmpfile stable_packages_versions.txt

typehint:
	$(ACTIVATE_VENV) && mypy $(DIR_ARGS)

lint:
	$(ACTIVATE_VENV) && pylint $(DIR_ARGS)

format:
	$(ACTIVATE_VENV) && black $(DIR_ARGS)

test_parallel: rust_workers  start_celery_workers
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest -n $(MANUAL_CORES) tests/
	-make stop_celery_workers

test: rust_workers start_celery_workers
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest tests/
	-make stop_celery_workers

coverage: rust_workers start_celery_workers
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest --cov-report term-missing --cov=. --cov-report html tests/
	make stop_celery_workers

coverage_parallel: rust_workers start_celery_workers
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) pytest --cov-report term-missing --cov=. -n $(MANUAL_CORES) tests/
	make stop_celery_workers

start_production: start_services start_celery_workers rust_workers
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_PROD) gunicorn app.app:app --workers $(CORES) --preload -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:$(PORT)

start_development: start_services rust_workers start_celery_workers
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) uvicorn app.app:app --host 0.0.0.0 --port $(PORT) --reload

# make sure to login to ngrok so it can server html responses
make ngrok:
	ngrok http $(PORT)

start_celery_workers:
	$(ACTIVATE_VENV) && ENV_FILE=$(ENV_FILE_USER) celery -A celery_worker worker --loglevel=info --detach

stop_celery_workers:
	pkill -f celery_worker

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
	docker compose --env-file $(ENV_FILE_USER) up -d $(SERVICES)

start_full_services:
	docker compose --env-file $(ENV_FILE_USER) up -d $(FULL_SERVICES)

stop_services:
	docker compose --env-file $(ENV_FILE_USER) stop $(SERVICES)

sr_services:
	docker compose --env-file $(ENV_FILE_USER) down

docker_clean:
	docker system prune -af

docker_update:
	docker compose --env-file $(ENV_FILE_USER) pull
	make start_services

env_file:
	cp $(ENV_FILE_DEV) $(ENV_FILE_USER)

bare_bones: env_file venv_create start_services test_parallel sr_services

soft_checklist: typehint coverage lint
hard_checklist: format lint typehint test coverage

install_rust:
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
	export PATH="$(HOME)/.cargo/bin:$(PATH)"

rust_workers:
	PATH="$(HOME)/.cargo/bin:$(PATH)" $(ACTIVATE_VENV) && cd celery_rust_workers && maturin develop
