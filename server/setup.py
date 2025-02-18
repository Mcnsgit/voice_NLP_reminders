from setuptools import setup, find_packages

setup(
    name="task-manager",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "asyncpg",
        "python-jose",
        "passlib",
        "python-multipart",
        "pydantic",
        "pydantic-settings",
        "redis",
    ],
)
