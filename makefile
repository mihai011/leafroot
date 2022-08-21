ACTIVATE_VENV=. venv/bin/activate
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/

CORES=`nproc`
MANUAL_CORES=4
	

venv_create: requirements.txt
	python3 -m venv venv
	$(ACTIVATE_VENV) &&  pip install -r requirements.txt

venv_delete:
	rm -rf venv/

venv_update:
	$(ACTIVATE_VENV) && pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U 
	pip freeze > requirements.txt
	
typehint: 
	$(ACTIVATE_VENV) &&mypy $(DIR_ARGS)

test_parallel: 
	$(ACTIVATE_VENV) && ENV=dev pytest -n $(MANUAL_CORES) tests/

test: 
	$(ACTIVATE_VENV) && ENV=dev pytest tests/

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

start_db:
	docker-compose up -d db

soft_checklist: typehint coverage lint  
hard_checklist: format lint typehint test coverage
