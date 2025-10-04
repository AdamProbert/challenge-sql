# Pokemon SQL Trainer: Learning with the Pokedex

This repository contains a series of progressive challenges designed to help you learn SQL fundamentals with no prior knowledge. The challenges are themed around building and using a Pokedex database, starting from basic SELECT statements and working up to complex queries that Professor Oak himself would be proud of!

![image](https://github.com/user-attachments/assets/caf62775-2449-4a7f-9507-9b09460b146e)


## Prerequisites

- Docker (for running the PostgreSQL database)
- pyenv (for managing Python versions)
- Python 3.11 (for the Pokedex interface)

## Installation

1. Clone this repository:
```bash
git clone git@github.com:AdamProbert/challenge-sql.git
cd challenge-sql
```

2. Set up Python environment with pyenv:
```bash
# Install Python 3.11 if you don't have it already
pyenv install 3.11.4

# Create a virtual environment for this project
pyenv virtualenv 3.11.4 pokemon-sql

# Activate the virtual environment
pyenv local pokemon-sql
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Start the services using Docker (database + FastAPI API + React frontend):
```bash
docker compose up --build
```

Then open http://localhost:5173 to launch the browser-based trainer. The API is available at http://localhost:8000 (interactive docs at http://localhost:8000/docs).

If you only want the CLI experience, you can start just the database instead:

```bash
docker compose up -d db
```

This will start a PostgreSQL database with pre-loaded Pokemon data for the challenges.

## Running Challenges

To start the Pokedex interface:

```bash
python challenge.py
```

You can also run a specific challenge:

```bash
python challenge.py --challenge 1
```

Or check your solution:

```bash
python challenge.py --check solution.sql
```

To run all challenge tests:

```bash
python challenge.py --test-all
```

## Web Application Overview

The new web interface mirrors the CLI journey in a browser-friendly experience built with FastAPI, React, Mantine, and the Monaco editor. Highlights:

- Browse the full catalogue of challenges grouped by difficulty
- Render rich markdown instructions, hints, and expected columns
- Inspect the per-challenge database schema for your current sandbox
- Run ad-hoc SQL securely within an isolated Postgres schema per browser session
- Validate your solution against the canonical answer without leaving the page
- Local progress is stored in the browser so you can resume where you left off

### Development workflow

The default `docker compose up --build` command runs everything you need (database, API with live reload, and Vite dev server). If you prefer to work on pieces individually:

- **API** (FastAPI + PostgreSQL)
    ```powershell
    cd web\api
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

- **Frontend** (React + Vite + Mantine)
    ```powershell
    cd web\frontend
    npm install
    npm run dev
    ```

Set `VITE_API_BASE_URL` to point at the API origin if you are not using the docker-compose proxy (defaults to `/api`).

## Web Application Overview

The new web interface mirrors the CLI journey in a browser-friendly experience built with FastAPI, React, Mantine, and Monaco Editor. Highlights:

- Browse the full catalogue of challenges grouped by difficulty
- Render rich markdown instructions, hints, and expected columns
- Inspect the database schema provisioned per challenge
- Run ad-hoc SQL securely within an isolated Postgres schema per session
- Validate your solution against the canonical answer without leaving the page
- Progress is stored locally in the browser so you can resume where you left off

### Development workflow

The default `docker compose up --build` command runs everything you need (database, API with live reload, and Vite dev server). If you prefer to work on pieces individually:

- **API** (FastAPI + PostgreSQL)
    ```bash
    cd web/api
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

- **Frontend** (React + Vite + Mantine)
    ```bash
    cd web/frontend
    npm install
    npm run dev
    ```

The frontend expects `VITE_API_BASE_URL` to point at the API origin (defaults to `/api`, which works with the docker-compose proxy configuration).

## Challenges

The challenges are organized by difficulty:

1. **Beginner**: Basic SELECT statements, WHERE clauses, and simple filtering - just like your starter Pokemon
2. **Intermediate**: Joins, aggregations, Subqueries, and GROUP BY - evolving your SQL skills

Each challenge provides:
- A clear description of the task
- Sample Pokemon data to work with
- Expected output
- Hints if you get stuck

## Project Structure

```
challenges/               # Challenge definitions and SQL files
├── beginner/             # Beginner challenges
│   ├── 01/               # First beginner challenge
│   │   ├── challenge.yaml  # Challenge definition
│   │   ├── setup.sql       # SQL to set up tables and data
│   │   └── solution.sql    # Solution for validation
│   └── 02/               # Second beginner challenge
├── intermediate/         # Intermediate challenges
└── advanced/             # Advanced challenges

pokedex/                  # Python package containing the application code
├── __init__.py           # Package initialization
├── db.py                 # Database connection handling
├── ui.py                 # User interface components
├── challenge_loader.py   # Challenge loading functionality
├── validator.py          # Challenge validation
└── challenge_runner.py   # Challenge execution logic

.github/                  # GitHub configurations
└── workflows/            # GitHub Actions workflows
    └── run-tests.yml     # Workflow to run all challenge tests

challenge.py                    # Command-line interface entry point
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to add new challenges or improve existing ones.

## Continuous Integration

This project uses GitHub Actions to automatically run all challenge tests on every push to ensure that challenges remain valid as the codebase evolves.
