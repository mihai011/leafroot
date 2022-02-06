typehint:
	mypy app/ controllers/ data/ tests/ scripts/ utils/


test:
	pytest tests/


lint:
	pylint app/ controllers/ data/ tests/ scripts/ utils/


format:
	black app/ controllers/ data/ tests/ scripts/ utils/


checklist: format lint typehint test