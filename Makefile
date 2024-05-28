run:
	uvicorn main:app --reload --port 8000

makemigration:
	alembic revision --autogenerate -m "${m}"

migrate:
	alembic upgrade head