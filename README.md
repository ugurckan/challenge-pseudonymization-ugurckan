# Patient pseudonymization

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the script

```bash
python main.py
```

This reads `patients.csv` and generates `pii.csv` and `health.csv`.

## Running the tests

```bash
pytest -v
```
