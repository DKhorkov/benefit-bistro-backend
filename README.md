# Benefit Bistro

All commands should be executed in project's root directory:

## Before start:
Due to the fact, that DockerHub doesn't work in Russia now, you need to copy the ```daemon.json``` file
to one of the following directories depending on your system:

```
Linux, regular setup:    /etc/docker/daemon.json
Linux, rootless mode:    ~/.config/docker/daemon.json
Windows:                 C:\ProgramData\docker\config\daemon.json
```

After completing the previous step, you must restart your computer for the changes to Docker to take effect. 

## Getting started

Only at first launch:
```bash
make -C docker network
```

### Run via docker:

To run app and it's dependencies in docker, use next command:
```bash
make -C docker prod
```


### Run via source files:

To run app via source files, first of all, use next command to launch app's dependencies:
```bash
make -C docker local
```

To run application via source files, use next commands:

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements/prod.txt

uvicorn src.app:app --env-file .env --host <Ypur host here> --port <Your por here> --reload 
```

### Run via IDE:

To run app via IDE, first of all, use next command to launch app's dependencies:
```bash
make -C docker local
```

Only for local development set the permissions to launch debugger:

```bash
sudo chmod -R 777 database_data
sudo chmod -R 777 database_backups
```

Run ```src/main.py``` file, using project's root directory as Working Directory and 
provide path to .env.local file as the environments file.

## Linters

```bash
flake8 ./ -v
```

## Type Checkers

```bash
mypy ./
```

## Alembic

### Run via docker, when app is launched in docker:

To create new migration use next command:
```bash
make -C docker makemigrations name=<your migration description here>
```

To migrate use next command:
```bash
make -C docker migrate
```

To downgrade database use next command:
```bash
make -C docker downgrade to=<Number of migrations>  # -1, -2 or base to downgrade to start point
```


### Run using source files:

To run alembic migrations for local database, use next command first:

```bash
export LOCAL_LAUNCH=true
```

To create new migration use next command:
```bash
alembic revision -m "<your migration description here>" --autogenerate
```

To migrate use next command:
```bash
alembic upgrade head
```

To downgrade database use next command:
```bash
alembic downgrade <Number of migrations>  # -1, -2 or base to downgrade to start point
```

## Tests

To run tests use next command in project's root directory:
```bash
pytest -v
```

To check tests coverage use next commands in project's root directory and 
open ```htmlcov/index.html``` file in browser:
```bash
coverage run -m pytest -v
coverage html
```


## Redis:

To stop already running redis-server use next command:
```bash
sudo service redis-server stop
```
