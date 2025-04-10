"""
Challenge validation utilities
"""

import os
from rich.console import Console

console = Console()

def run_validation(conn, challenge, user_sql, db_module):
    """Validate the user's SQL solution against the expected result."""
    validation = challenge.get('challenge', {}).get('validation', {})
    
    if validation.get('type') == 'result_set':
        # Run the user's query
        user_columns, user_results = db_module.execute_query(conn, user_sql)
        if isinstance(user_results, str):
            return False, f"Error in your SQL: {user_results}"
            
        # Run the solution query
        solution_file = os.path.join(challenge['dir'], validation.get('file'))
        if not os.path.exists(solution_file):
            return False, "Solution file not found. Please contact the challenge administrator."
            
        with open(solution_file, 'r') as f:
            solution_sql = f.read()
        solution_columns, solution_results = db_module.execute_query(conn, solution_sql)
        
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
        user_columns, user_results = db_module.execute_query(conn, user_sql)
        if isinstance(user_results, str):
            return False, f"Error in your SQL: {user_results}"
            
        expected_count = validation.get('count')
        if len(user_results) != expected_count:
            return False, f"Expected {expected_count} rows, but got {len(user_results)}."
            
        return True, f"Success! Your query returns the expected number of rows ({expected_count})."
            
    return False, "Validation type not supported."

def check_solution(challenge, solution_file, conn, db_module):
    """Check if a solution file is correct for a given challenge."""
    if not os.path.exists(solution_file):
        console.print(f"[bold red]Solution file {solution_file} not found.[/bold red]")
        return False
        
    with open(solution_file, 'r') as f:
        user_sql = f.read()
        
    if not db_module.setup_challenge_database(conn, challenge):
        return False
        
    success, message = run_validation(conn, challenge, user_sql, db_module)
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
                
    return success

def validate_solution_file(solution_file, challenge, conn, db_module):
    """Validate that a solution file correctly solves its own challenge."""
    if not os.path.exists(solution_file):
        return False, f"Solution file {solution_file} not found."
        
    try:
        with open(solution_file, 'r') as f:
            solution_sql = f.read()
        
        # Validate that the solution works against itself
        # This is a special case where we're testing that the solution matches its own expected output
        user_columns, user_results = db_module.execute_query(conn, solution_sql)
        
        if isinstance(user_results, str):
            return False, f"Error in solution SQL: {user_results}"
        
        # For result_set validation, just check if the query executes successfully
        # since we're comparing the solution against itself
        return True, "Solution executes successfully"
        
    except Exception as e:
        return False, f"Error validating solution: {e}"
