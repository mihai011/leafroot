SOURCE_VENV=source venv/bin/activate
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/

CORES=`nproc`
VENV_NAME?=venv

activate_venv: $(VENV_NAME)/bin/activate

venv_create: activate_venv requirements.txt
	python3 -m venv venv
	pip install -r requirements.txt

venv_delete:
	rm -rf venv/

venv_update: activate_venv
	pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U 
	pip freeze > requirements.txt
	
typehint: activate_venv
	mypy $(DIR_ARGS)

test_parallel: activate_venv
	ENV=dev pytest -n auto tests/

test: activate_venv
	ENV=dev pytest tests/

lint: activate_venv
	pylint $(DIR_ARGS)

format: activate_venv
	black $(DIR_ARGS)

coverage: activate_venv
	ENV=dev pytest --cov-report term-missing --cov=.  tests/

coverage_parallel: activate_venv
	ENV=dev pytest --cov-report term-missing --cov=. -n $(CORES) tests/

start_production: activate_venv
	ENV=prod gunicorn app.app:app --workers $(CORES) -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0 

start_development: activate_venv
	ENV=dev uvicorn app.app:app --host 0.0.0.0 --reload

soft_checklist: typehint coverage lint  
hard_checklist: format lint typehint test coverage
