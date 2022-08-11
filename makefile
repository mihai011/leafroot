SOURCE_VENV=. venv/bin/activate
DIR_ARGS = app/ controllers/ data/ tests/ scripts/ utils/

venv_create: requirements.txt
	python3 -m venv venv
	$(SOURCE_VENV) && pip install -r requirements.txt

venv_delete:
	rm -rf venv/

venv_update:
	$(SOURCE_VENV) && pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U 
	pip freeze > requirements.txt
	
typehint:
	$(SOURCE_VENV) && mypy $(DIR_ARGS)

test_parallel: 
	$(SOURCE_VENV) && pytest -n auto tests/

test_simple: 
	$(SOURCE_VENV) && pytest tests/

lint: 
	$(SOURCE_VENV) && pylint $(DIR_ARGS)

format: 
	$(SOURCE_VENV) && black $(DIR_ARGS)

coverage: 
	$(SOURCE_VENV) && pytest --cov-report term-missing --cov=.  tests/

coverage_parallel: 
	$(SOURCE_VENV) && pytest --cov-report term-missing --cov=. -n 2 tests/

start_production:
	$(SOURCE_VENV) && ENV=prod gunicorn app.app:app --workers 12 -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0 

start_development:
	$(SOURCE_VENV) && ENV=dev uvicorn app.app:app --host 0.0.0.0 --reload

# start_local: 
# 	$(SOURCE_VENV) && uvicorn app.app:app --reload

soft_checklist: typehint coverage lint  
hard_checklist: format lint typehint test coverage
