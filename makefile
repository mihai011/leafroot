ACTIVATE_VENV=. venv/bin/activate
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/ cache/

CORES=`nproc`
MANUAL_CORES=4


venv_create: venv_delete requirements.txt
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
	$(ACTIVATE_VENV) && ENV=dev pytest -n $(MANUAL_CORES) tests/
	make stop_celery_worker

test: start_celery_worker
	$(ACTIVATE_VENV) && ENV=dev pytest tests/
	make stop_celery_worker

lint:
	$(ACTIVATE_VENV) && pylint $(DIR_ARGS)

format:
	$(ACTIVATE_VENV) && black $(DIR_ARGS)

coverage:
	$(ACTIVATE_VENV) && ENV=dev pytest --cov-report term-missing --cov=.  tests/

coverage_parallel:
	$(ACTIVATE_VENV) && ENV=dev pytest --cov-report term-missing --cov=. -n $(CORES) tests/

start_production: venv_create
	$(ACTIVATE_VENV) && ENV=prod gunicorn app.app:app --workers $(CORES) -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0

start_development:
	$(ACTIVATE_VENV) && ENV=dev uvicorn app.app:app --host 0.0.0.0 --reload

start_celery_worker:
	$(ACTIVATE_VENV) && ENV=dev celery -A celery_worker worker --loglevel=info --detach

stop_celery_worker:
	$(ACTIVATE_VENV) && python scripts/stop_celery_workers.py

start_db:
	docker-compose up -d db

bandit:
	$(ACTIVATE_VENV) && bandit -r $(DIR_ARGS)

pydocstyle:
	$(ACTIVATE_VENV) && pydocstyle  $(DIR_ARGS)

soft_checklist: typehint coverage lint
hard_checklist: format lint typehint test coverage
