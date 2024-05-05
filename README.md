# Benefit Bistro

## Getting started

### Run via docker:

To run application via docker, use next command line in 
project's root directory:

Only at first launch:
```bash
make -C docker network
```

```bash
make -C docker local
```
or
```bash
make -C docker prod
```

### Run using source files:

To run application using source files, use next commands 
in project's root directory:

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn src.app:app --env-file .env --host <Ypur host here> --port <Your por here> --reload 
```

### Run via IDE:

Only for local development set the permissions to launch debugger:

```bash
sudo chmod -R 777 database_data
sudo chmod -R 777 database_backups
```

Run ```src/main.py``` file, using project's root directory as Working Directory and 
provide path to .env.local file as the environments file.

## Linters

```bash
flake8 ./src -v
```

## Type Checkers

```bash
mypy ./src
```


## Alembic

### Run via docker, when app is launched in docker:

To create new migration run next command:
```bash
make -C docker makemigrations name=<your migration description here>
```

To migrate run next command:
```bash
make -C docker migrate
```

To downgrade database run next command:
```bash
make -C docker downgrade to=<Number of migrations>  # -1, -2 or base to downgrade to start point
```


### Run using source files:

To run alembic migrations for local database, user next command first:

```bash
export LOCAL_LAUNCH=true
```

To create new migration run next command:
```bash
alembic revision -m "<your migration description here>" --autogenerate
```

To migrate run next command:
```bash
alembic upgrade head
```

To downgrade database run next command:
```bash
alembic downgrade <Number of migrations>  # -1, -2 or base to downgrade to start point
```

## Tests

To run tests use next command in project's root directory:
```bash
pytest -v
```

To check tests coverage user next commands in project's root directory and 
open ```htmlcov/index.html``` file in browser:
```bash
coverage run -m pytest
coverage html
```
