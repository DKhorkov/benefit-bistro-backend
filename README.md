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

uvicorn src.main:app --host <Ypur host here> --port <Your por here> --reload
```

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
