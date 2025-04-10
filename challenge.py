#!/usr/bin/env python3.11
"""
Pokemon SQL Trainer - Command Line Interface
This script provides a command-line interface for users to interact with SQL learning challenges.
"""

import argparse
import os
import sys
import yaml
import re
import psycopg2
import signal
import readline
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box
import colorama

colorama.init()
console = Console()

# Database connection parameters
DB_PARAMS = {
    'dbname': 'sqlchallenge',
    'user': 'sqlchallenge',
    'password': 'sqlchallenge',
    'host': 'localhost',
    'port': 5432
}

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    console.print("\n[bold yellow]Exiting Pokemon SQL Trainer. Keep training to become a SQL Master![/bold yellow]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        console.print(f"[bold red]Error connecting to Pokedex database: {e}[/bold red]")
        sys.exit(1)

def validate_challenge_directories(difficulty):
    """Validate that challenge directories are sequentially numbered."""
    challenge_dir = os.path.join('challenges', difficulty)
    if not os.path.exists(challenge_dir):
        return True
    
    # Find all numbered directories
    numbered_dirs = []
    for dirname in os.listdir(challenge_dir):
        if os.path.isdir(os.path.join(challenge_dir, dirname)) and dirname.isdigit():
            numbered_dirs.append(int(dirname))
    
    if not numbered_dirs:
        return True
    
    # Check if directories are sequential
    numbered_dirs.sort()
    expected_nums = list(range(1, len(numbered_dirs) + 1))
    expected_dirs = [str(num).zfill(2) for num in expected_nums]
    actual_dirs = [str(num).zfill(2) for num in numbered_dirs]
    
    if numbered_dirs != expected_nums:
        console.print(f"[bold yellow]Warning: Challenge directories for {difficulty} difficulty are not sequential.[/bold yellow]")
        console.print(f"[yellow]Found: {', '.join(actual_dirs)}[/yellow]")
        console.print(f"[yellow]Expected: {', '.join(expected_dirs)}[/yellow]")
        return False
    
    return True

def load_challenges():
    """Load all challenge definitions from YAML files in numbered directories."""
    challenges = []
    
    for difficulty in ['beginner', 'intermediate', 'advanced']:
        # Validate directory structure
        validate_challenge_directories(difficulty)
        
        challenge_dir = os.path.join('challenges', difficulty)
        if not os.path.exists(challenge_dir):
            continue
            
        # Get all numbered directories
        subdirs = []
        for dirname in os.listdir(challenge_dir):
            dir_path = os.path.join(challenge_dir, dirname)
            if os.path.isdir(dir_path) and dirname.isdigit():
                subdirs.append((int(dirname), dir_path))
                
        # Sort directories by number
        subdirs.sort()
        
        # Load challenge from each directory
        for _, dir_path in subdirs:
            challenge_file = os.path.join(dir_path, 'challenge.yaml')
            
            if os.path.exists(challenge_file):
                try:
                    with open(challenge_file, 'r') as file:
                        challenge = yaml.safe_load(file)
                        challenge['file_path'] = challenge_file
                        challenge['dir'] = dir_path
                        challenges.append(challenge)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not load challenge {challenge_file}: {e}[/yellow]")
    
    # Sort by difficulty
    difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
    challenges.sort(key=lambda x: difficulty_order.get(x.get('difficulty'), 999))
    return challenges

def execute_query(conn, query_sql):
    """Execute SQL query and return results."""
    cursor = conn.cursor()
    try:
        # Add semicolon if user didn't include one
        if not query_sql.strip().endswith(';'):
            query_sql += ';'
            
        cursor.execute(query_sql)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return columns, results
        return None, []
    except Exception as e:
        # Roll back the transaction to clear the error state
        conn.rollback()
        return None, str(e)
    finally:
        cursor.close()

def setup_challenge_database(conn, challenge):
    """Set up database tables and data for a challenge."""
    cursor = conn.cursor()
    try:
        # Reset database - drop all tables in public schema
        cursor.execute("""
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        conn.commit()
        
        # Run setup SQL files
        for setup_file in challenge.get('setup', []):
            file_path = os.path.join(challenge['dir'], setup_file.get('file'))
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    setup_sql = f.read()
                cursor.execute(setup_sql)
                conn.commit()
            else:
                console.print(f"[bold red]Error: Setup file {file_path} not found[/bold red]")
                return False
        return True
    except Exception as e:
        console.print(f"[bold red]Error setting up challenge database: {e}[/bold red]")
        return False
    finally:
        cursor.close()

def run_validation(conn, challenge, user_sql):
    """Validate the user's SQL solution against the expected result."""
    validation = challenge.get('challenge', {}).get('validation', {})
    
    if validation.get('type') == 'result_set':
        # Run the user's query
        user_columns, user_results = execute_query(conn, user_sql)
        if isinstance(user_results, str):
            return False, f"Error in your SQL: {user_results}"
            
        # Run the solution query
        solution_file = os.path.join(challenge['dir'], validation.get('file'))
        if not os.path.exists(solution_file):
            return False, "Solution file not found. Please contact the challenge administrator."
            
        with open(solution_file, 'r') as f:
            solution_sql = f.read()
        solution_columns, solution_results = execute_query(conn, solution_sql)
        
        # Compare results
        if user_columns != solution_columns:
            missing = set(solution_columns) - set(user_columns or [])
            extra = set(user_columns or []) - set(solution_columns)
            error_msg = "Column mismatch:\n"
            if missing:
                error_msg += f"Missing columns: {', '.join(missing)}\n"
            if extra:
                error_msg += f"Extra columns: {', '.join(extra)}\n"
            return False, error_msg
            
        if sorted(user_results) != sorted(solution_results):
            return False, "Results don't match the expected output."
            
        return True, "Success! Your query produces the expected results."
            
    elif validation.get('type') == 'row_count':
        user_columns, user_results = execute_query(conn, user_sql)
        if isinstance(user_results, str):
            return False, f"Error in your SQL: {user_results}"
            
        expected_count = validation.get('count')
        if len(user_results) != expected_count:
            return False, f"Expected {expected_count} rows, but got {len(user_results)}."
            
        return True, f"Success! Your query returns the expected number of rows ({expected_count})."
            
    return False, "Validation type not supported."

def display_table(columns, rows):
    """Display query results as a table."""
    if not columns or not rows:
        console.print("[yellow]Query returned no results.[/yellow]")
        return
        
    table = Table(show_header=True, header_style="bold", box=box.SIMPLE)
    for column in columns:
        table.add_column(column)
        
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
        
    console.print(table)

def show_challenge(challenge):
    """Display challenge information."""
    console.print(Panel(f"[bold]Challenge: {challenge.get('title')}[/bold]", 
                       subtitle=f"Difficulty: {challenge.get('difficulty')}"))
    
    # Display description (tutorial part)
    console.print(Markdown(challenge.get('description', '')))
    
    # Highlight the task better using markdown heading
    console.print(Markdown("## Your Task:"))
    console.print(Markdown(challenge.get('challenge', {}).get('task', '')))
    
    # Show expected columns
    expected_columns = challenge.get('challenge', {}).get('expected_columns', [])
    if expected_columns:
        console.print("\n[bold]Expected Columns:[/bold]")
        for col in expected_columns:
            console.print(f"- {col}")
    
    # Show database schema
    console.print("\n[bold]Available Tables:[/bold]")
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        
        current_table = None
        for table, column, dtype in cursor.fetchall():
            if table != current_table:
                console.print(f"\n[bold]{table}[/bold]")
                current_table = table
            console.print(f"  - {column} ({dtype})")
                
    except Exception as e:
        console.print(f"[red]Error retrieving Pokedex schema: {e}[/red]")
    finally:
        conn.close()

def show_table_data(conn):
    """Display the data of a selected table."""
    try:
        cursor = conn.cursor()
        
        # Get list of available tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            console.print("[yellow]No tables found in the database.[/yellow]")
            return
            
        # Show table selection menu
        console.print("\n[bold]Available Tables:[/bold]")
        for i, table in enumerate(tables, 1):
            console.print(f"{i}. {table}")
            
        console.print("\nEnter the number of the table you want to view (or 'b' to go back):")
        selection = input("> ")
        
        if selection.lower() == 'b':
            return
            
        try:
            table_index = int(selection) - 1
            if table_index < 0 or table_index >= len(tables):
                console.print("[bold red]Invalid selection.[/bold red]")
                return
                
            selected_table = tables[table_index]
            
            # Execute query to get all data from the table
            cursor.execute(f"SELECT * FROM {selected_table} LIMIT 100;")
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            
            console.print(f"\n[bold]Data from table '{selected_table}':[/bold]")
            display_table(columns, results)
            
            if len(results) == 100:
                console.print("[yellow]Note: Only showing first 100 rows.[/yellow]")
                
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Error retrieving table data: {e}[/bold red]")

def check_solution(challenge_num, solution_file):
    """Check if a solution file is correct for a given challenge."""
    challenges = load_challenges()
    
    if challenge_num < 1 or challenge_num > len(challenges):
        console.print(f"[bold red]Challenge {challenge_num} not found. Available challenges: 1-{len(challenges)}[/bold red]")
        return
        
    challenge = challenges[challenge_num - 1]
    
    if not os.path.exists(solution_file):
        console.print(f"[bold red]Solution file {solution_file} not found.[/bold red]")
        return
        
    with open(solution_file, 'r') as f:
        user_sql = f.read()
        
    conn = connect_to_db()
    try:
        if not setup_challenge_database(conn, challenge):
            return
            
        success, message = run_validation(conn, challenge, user_sql)
        if success:
            console.print(f"[bold green]{message}[/bold green]")
        else:
            console.print(f"[bold red]{message}[/bold red]")
            
            # Show hints if available
            hints = challenge.get('challenge', {}).get('hints', [])
            if hints and not success:
                console.print("\n[bold yellow]Hints:[/bold yellow]")
                for i, hint in enumerate(hints, 1):
                    console.print(f"[yellow]{i}. {hint}[/yellow]")
    finally:
        conn.close()

def interactive_mode(challenge_num=None):
    """Run the challenge interface in interactive mode."""
    challenges = load_challenges()
    
    if not challenges:
        console.print("[bold red]No challenges found. Check the 'challenges' directory.[/bold red]")
        return
        
    if challenge_num is not None:
        if challenge_num < 1 or challenge_num > len(challenges):
            console.print(f"[bold red]Challenge {challenge_num} not found. Available challenges: 1-{len(challenges)}[/bold red]")
            return
        current_challenge = challenge_num - 1
    else:
        # Show challenge list
        console.print("[bold]Available Pokemon SQL Challenges:[/bold]")
        for i, challenge in enumerate(challenges, 1):
            console.print(f"{i}. [{challenge.get('difficulty')}] {challenge.get('title')}")
            
        # Ask user to select a challenge
        console.print("\nEnter the number of the challenge you want to try (or 'q' to quit):")
        selection = input("> ")
        
        if selection.lower() == 'q':
            return
            
        try:
            current_challenge = int(selection) - 1
            if current_challenge < 0 or current_challenge >= len(challenges):
                console.print("[bold red]Invalid selection.[/bold red]")
                return
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")
            return
    
    challenge = challenges[current_challenge]
    
    conn = connect_to_db()
    try:
        if not setup_challenge_database(conn, challenge):
            return
            
        while True:
            console.clear()
            show_challenge(challenge)
            
            console.print("\n[bold]Enter your SQL query (or 'q' to quit, 'h' for hint, 'v' to view table data):[/bold]")
            console.print("[italic yellow](End your SQL query with a semicolon and press Enter to submit)[/italic yellow]")
            
            user_sql = ""
            lines = []
            while True:
                try:
                    line = input()
                    # Handle single-letter commands immediately - no semicolon required
                    if line.lower() in ['q', 'h', 'v']:
                        user_sql = line.lower()
                        break
                        
                    lines.append(line)
                    user_sql = "\n".join(lines)
                    
                    # If line contains semicolon, we can execute the SQL
                    if ';' in line:
                        break
                except EOFError:
                    break
                    
            if user_sql == 'q':
                break
                
            if user_sql == 'v':
                show_table_data(conn)
                input("\nPress Enter to continue...")
                continue
                
            if user_sql == 'h':
                hints = challenge.get('challenge', {}).get('hints', [])
                if hints:
                    console.print("\n[bold yellow]Pokedex Hints:[/bold yellow]")
                    for i, hint in enumerate(hints, 1):
                        console.print(f"[yellow]{i}. {hint}[/yellow]")
                else:
                    console.print("[yellow]No hints available for this challenge.[/yellow]")
                input("\nPress Enter to continue...")
                continue
                
            if user_sql.strip():
                try:
                    # Execute the user's query and display results
                    columns, results = execute_query(conn, user_sql)
                    
                    if isinstance(results, str):
                        console.print(f"[bold red]SQL Error: {results}[/bold red]")
                    else:
                        console.print("\n[bold]Pokedex Results:[/bold]")
                        display_table(columns, results)
                        
                        # Validate the query
                        success, message = run_validation(conn, challenge, user_sql)
                        if success:
                            console.print(f"[bold green]{message}[/bold green]")
                            
                            # If there's a next challenge, automatically proceed
                            if current_challenge < len(challenges) - 1:
                                console.print("\n[bold]Great work, Trainer! Press Enter to proceed to the next challenge.[/bold]")
                                input()
                                current_challenge += 1
                                challenge = challenges[current_challenge]
                                setup_challenge_database(conn, challenge)
                                continue
                            else:
                                console.print("\n[bold green]Congratulations! You've completed all Pokemon SQL challenges! You're ready to be a Pokemon SQL Master![/bold green]")
                        else:
                            console.print(f"[bold red]{message}[/bold red]")
                except Exception as e:
                    console.print(f"[bold red]Error: {e}[/bold red]")
                    
            input("\nPress Enter to continue...")
    finally:
        conn.close()

def test_challenge(challenge_file):
    """Test a challenge definition."""
    if not os.path.exists(challenge_file):
        console.print(f"[bold red]Challenge file {challenge_file} not found.[/bold red]")
        return
        
    try:
        with open(challenge_file, 'r') as file:
            challenge = yaml.safe_load(file)
            challenge['file_path'] = challenge_file
            challenge['dir'] = os.path.dirname(challenge_file)
            
        console.print(f"[bold]Testing Challenge: {challenge.get('title')}[/bold]")
        
        # Validate required fields
        required_fields = [
            'title', 'description', 'difficulty', 'setup', 
            'challenge.task', 'challenge.validation'
        ]
        
        for field in required_fields:
            parts = field.split('.')
            obj = challenge
            for part in parts:
                if isinstance(obj, dict) and part in obj:
                    obj = obj[part]
                else:
                    console.print(f"[bold red]Missing required field: {field}[/bold red]")
                    return
        
        # Validate setup files exist
        for setup_file in challenge.get('setup', []):
            file_path = os.path.join(challenge['dir'], setup_file.get('file'))
            if not os.path.exists(file_path):
                console.print(f"[bold red]Setup file does not exist: {file_path}[/bold red]")
                return
                
        # Validate solution file exists if result_set validation
        validation = challenge.get('challenge', {}).get('validation', {})
        if validation.get('type') == 'result_set':
            solution_file = os.path.join(challenge['dir'], validation.get('file'))
            if not os.path.exists(solution_file):
                console.print(f"[bold red]Solution file does not exist: {solution_file}[/bold red]")
                return
                
        console.print("[bold green]Challenge definition looks valid![/bold green]")
        
        # Test database setup and solution
        conn = connect_to_db()
        try:
            console.print("[bold]Setting up challenge database...[/bold]")
            if not setup_challenge_database(conn, challenge):
                console.print("[bold red]Failed to set up challenge database.[/bold red]")
                return
                
            console.print("[bold green]Database setup successful![/bold green]")
            
            # If solution file exists, test it
            if validation.get('type') == 'result_set':
                solution_file = os.path.join(challenge['dir'], validation.get('file'))
                with open(solution_file, 'r') as f:
                    solution_sql = f.read()
                    
                console.print("[bold]Testing solution...[/bold]")
                columns, results = execute_query(conn, solution_sql)
                if isinstance(results, str):
                    console.print(f"[bold red]Error in solution SQL: {results}[/bold red]")
                else:
                    console.print("[bold green]Solution executes successfully![/bold green]")
                    console.print("\n[bold]Solution Results:[/bold]")
                    display_table(columns, results)
        finally:
            conn.close()
            
    except Exception as e:
        console.print(f"[bold red]Error testing challenge: {e}[/bold red]")

def main():
    parser = argparse.ArgumentParser(description='Pokemon SQL Trainer Challenge')
    parser.add_argument('--challenge', type=int, help='Specific challenge number to run')
    parser.add_argument('--check', metavar='FILE', help='Check if a SQL file solves the specified challenge')
    parser.add_argument('--test-challenge', metavar='FILE', help='Test a challenge YAML definition')
    
    args = parser.parse_args()
    
    if args.test_challenge:
        test_challenge(args.test_challenge)
    elif args.check:
        if not args.challenge:
            console.print("[bold red]Error: --challenge must be specified with --check[/bold red]")
            return
        check_solution(args.challenge, args.check)
    else:
        interactive_mode(args.challenge)

if __name__ == '__main__':
    main()
