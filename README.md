# Benefit Bistro

## Getting started

### Run via docker:

To run application via docker, use next command line in 
project's root directory:

```bash
make -C docker clean && make -C docker build && make -C docker run
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

### Linters

```bash
flake8 ./src -v
```

### Type Checkers

```bash
mypy ./src -v
```