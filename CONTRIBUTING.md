# Contributing to Pokemon SQL Trainer

Thank you for considering contributing to the Pokemon SQL Trainer repository! This document provides guidelines on how to add new challenges or improve existing ones.

## Development Environment Setup

Before contributing to the project, please set up your development environment:

```bash
# Install Python 3.11 using pyenv if you don't have it already
pyenv install 3.11.4

# Create a virtual environment for this project
pyenv virtualenv 3.11.4 pokemon-sql

# Activate the virtual environment
pyenv local pokemon-sql

# Install dependencies
pip install -r requirements.txt
```

## Challenge Directory Structure

Challenges are organized in the following structure:

```
challenges/
  beginner/
    01/
      challenge.yaml
      setup.sql
      solution.sql
    02/
      challenge.yaml
      setup.sql
      solution.sql
  intermediate/
    01/
      challenge.yaml
      setup.sql
      solution.sql
  advanced/
    01/
      challenge.yaml
      setup.sql
      solution.sql
```

Each challenge has its own numbered directory. The directory number determines the order of the challenges, starting from `01`. **Important:** Challenge directories must be sequentially numbered within each difficulty level (01, 02, 03, etc.) without gaps.

## Adding New Challenges

To add a new challenge:

1. Determine the appropriate difficulty level (beginner, intermediate, advanced)
2. Find the highest numbered directory in that difficulty level and create a new directory with the next sequential number
3. Create the following files in the new directory:

   - `challenge.yaml`: Challenge definition
   - `setup.sql`: SQL to set up tables and data
   - `solution.sql`: Solution for validation

4. Use the following template for the `challenge.yaml` file:

```yaml
title: "Your Challenge Title"
description: |
  Detailed description of what the challenge is about.
  You can include multiple paragraphs if needed.

difficulty: "beginner"  # or "intermediate" or "advanced"

# Database setup
setup:
  - file: "setup.sql"  # SQL to set up tables and data for this challenge

# Challenge details  
challenge:
  task: |
    Write a query that selects all Pokemon from the pokemon table
    where the level is greater than 50.
  
  expected_columns:
    - "pokemon_id"
    - "name"
    - "type"
    - "level"
  
  validation:
    type: "result_set"  # Can be "result_set", "row_count", or "custom"
    file: "solution.sql"  # Reference solution
  
  hints:
    - "Remember to use the WHERE clause to filter records"
    - "The comparison operator for 'greater than' is '>'"
```

**Note:** Unlike previous versions, you do not need to specify an `order` field in the YAML file, as the ordering is determined by the directory names.

## Testing Your Challenge

Before submitting a new challenge, make sure to test it:

```bash
python challenge.py --test-challenge path/to/your/challenge/challenge.yaml
```

The script will automatically validate that challenge directories are sequentially numbered and will warn if any inconsistencies are found.

## Code Style

- Follow PEP 8 guidelines for Python code
- SQL keywords should be in UPPERCASE for readability
- Include comments in your SQL to explain complex parts

## Pull Request Process

1. Fork the repository
2. Create a new branch (`git checkout -b my-new-challenge`)
3. Add your challenge files following the directory structure guidelines
4. Commit your changes (`git commit -am 'Add new advanced join challenge'`)
5. Push to the branch (`git push origin my-new-challenge`)
6. Create a new Pull Request

## Review Criteria

Challenges will be reviewed based on:
- Correctness and clarity of instructions
- Appropriate difficulty level
- Educational value
- Completeness of setup and validation
- Proper directory structure and naming

Thank you for contributing and helping others learn SQL!
