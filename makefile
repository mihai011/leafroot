typehint:
	mypy app/ controllers/ data/ tests/ scripts/ utils/

test_parallel:
	pytest -n auto test/

test_simple:
	pytest tests/

lint:
	pylint app/ controllers/ data/ tests/ scripts/ utils/

format:
	black app/ controllers/ data/ tests/ scripts/ utils/

coverage:
	coverage run --concurrency=greenlet -m pytest tests/ 
	coverage report -m

coverage_parallel:
	pytest --cov=controllers --concurrency=greenlet -n 2 tests/

start_production:
	gunicorn app.app:app --workers 12 -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0 

start_development:
	gunicorn app.app:app --workers 12 -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0 --reload

start_local:
	uvicorn app.app:app --reload

soft_checklist: typehint coverage lint  
hard_checklist: format lint typehint test coverage
