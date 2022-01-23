# fast-api-full
A FAST-API base project for fast development (imporving developer cycles);

Start:
gunicorn app.app:app --workers 12 -k uvicorn.workers.UvicornH11Worker --bind 0.0.0.0

Create migration and apply it:

alembic revision --autogenerate -m "<migration_message>"
alembic upgrade head


Test (pytest parallel for fast testing):
pytest -n <cores>
