.PHONY: db-init db-migrate db-upgrade de-downgrade

db-init:
	alembic init alembic

db-migrate:
	alembic revision --autogenerate -m "$(message)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1