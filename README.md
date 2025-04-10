# Pokemon SQL Trainer: Learning with the Pokedex

This repository contains a series of progressive challenges designed to help you learn SQL fundamentals with no prior knowledge. The challenges are themed around building and using a Pokedex database, starting from basic SELECT statements and working up to complex queries that Professor Oak himself would be proud of!

## Prerequisites

- Docker (for running the PostgreSQL database)
- pyenv (for managing Python versions)
- Python 3.11 (for the Pokedex interface)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/challenge-sql.git
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

4. Start the database using Docker:
```bash
docker-compose up -d
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

## Challenges

The challenges are organized by difficulty:

1. **Beginner**: Basic SELECT statements, WHERE clauses, and simple filtering - just like your starter Pokemon
2. **Intermediate**: Joins, aggregations, and GROUP BY - evolving your SQL skills
3. **Advanced**: Subqueries, window functions, and more complex operations - mastering SQL like a Pokemon Champion

Each challenge provides:
- A clear description of the task
- Sample Pokemon data to work with
- Expected output
- Hints if you get stuck

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to add new challenges or improve existing ones.

## License

MIT
