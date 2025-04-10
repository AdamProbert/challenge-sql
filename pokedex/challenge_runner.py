"""
Challenge execution logic
"""

import os
from rich.console import Console

console = Console()

def interactive_mode(challenge_num=None, db_module=None, ui_module=None, 
                     validator_module=None, challenge_loader_module=None):
    """Run the challenge interface in interactive mode."""
    challenges = challenge_loader_module.load_challenges()
    
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
    
    try:
        conn = db_module.connect_to_db()
    except Exception as e:
        console.print(f"[bold red]Failed to connect to the database: {e}[/bold red]")
        return
    
    try:
        if not db_module.setup_challenge_database(conn, challenge):
            return
            
        while True:
            console.clear()
            ui_module.show_challenge(challenge, conn, db_module)
            
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
                ui_module.show_table_data(conn, db_module)
                input("\nPress Enter to continue...")
                continue
                
            if user_sql == 'h':
                hints = challenge.get('challenge', {}).get('hints', [])
                ui_module.show_hints(hints)
                input("\nPress Enter to continue...")
                continue
                
            if user_sql.strip():
                try:
                    # Execute the user's query and display results
                    columns, results = db_module.execute_query(conn, user_sql)
                    
                    if isinstance(results, str):
                        console.print(f"[bold red]SQL Error: {results}[/bold red]")
                    else:
                        console.print("\n[bold]Pokedex Results:[/bold]")
                        ui_module.display_table(columns, results)
                        
                        # Validate the query
                        success, message = validator_module.run_validation(conn, challenge, user_sql, db_module)
                        if success:
                            console.print(f"[bold green]{message}[/bold green]")
                            
                            # If there's a next challenge, automatically proceed
                            if current_challenge < len(challenges) - 1:
                                console.print("\n[bold]Great work, Trainer! Press Enter to proceed to the next challenge.[/bold]")
                                input()
                                current_challenge += 1
                                challenge = challenges[current_challenge]
                                db_module.setup_challenge_database(conn, challenge)
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

def test_challenge(challenge_file, db_module=None, ui_module=None, 
                  validator_module=None, challenge_loader_module=None):
    """Test a challenge definition."""
    if not os.path.exists(challenge_file):
        console.print(f"[bold red]Challenge file {challenge_file} not found.[/bold red]")
        return
        
    try:
        with open(challenge_file, 'r') as file:
            import yaml
            challenge = yaml.safe_load(file)
            challenge['file_path'] = challenge_file
            challenge['dir'] = os.path.dirname(challenge_file)
            
        console.print(f"[bold]Testing Challenge: {challenge.get('title')}[/bold]")
        
        # Validate the challenge definition
        missing_fields = challenge_loader_module.validate_challenge(challenge)
        if missing_fields:
            console.print("[bold red]Challenge definition is invalid:[/bold red]")
            for field in missing_fields:
                console.print(f"[bold red]- Missing field: {field}[/bold red]")
            return
                
        console.print("[bold green]Challenge definition looks valid![/bold green]")
        
        # Test database setup and solution
        try:
            conn = db_module.connect_to_db()
        except Exception as e:
            console.print(f"[bold red]Failed to connect to the database: {e}[/bold red]")
            return
            
        try:
            console.print("[bold]Setting up challenge database...[/bold]")
            if not db_module.setup_challenge_database(conn, challenge):
                console.print("[bold red]Failed to set up challenge database.[/bold red]")
                return
                
            console.print("[bold green]Database setup successful![/bold green]")
            
            # If solution file exists, test it using the validator module
            validation = challenge.get('challenge', {}).get('validation', {})
            if validation.get('type') == 'result_set':
                solution_file = os.path.join(challenge['dir'], validation.get('file'))
                if os.path.exists(solution_file):
                    console.print("[bold]Testing solution...[/bold]")
                    # Use validator module to test the solution against itself
                    success, message = validator_module.validate_solution_file(solution_file, challenge, conn, db_module)
                    if success:
                        console.print("[bold green]Solution executes successfully![/bold green]")
                        
                        # Display the solution results
                        with open(solution_file, 'r') as f:
                            solution_sql = f.read()
                        columns, results = db_module.execute_query(conn, solution_sql)
                        if not isinstance(results, str):
                            console.print("\n[bold]Solution Results:[/bold]")
                            ui_module.display_table(columns, results)
                    else:
                        console.print(f"[bold red]Error validating solution: {message}[/bold red]")
                else:
                    console.print(f"[bold red]Solution file does not exist: {solution_file}[/bold red]")
        finally:
            conn.close()
            
    except Exception as e:
        console.print(f"[bold red]Error testing challenge: {e}[/bold red]")

def test_all(db_module=None, ui_module=None, validator_module=None, challenge_loader_module=None):
    """Test all challenge definitions in the challenges directory."""
    console.print("[bold]Testing all challenges...[/bold]")
    
    # Find all challenge.yaml files
    challenge_files = []
    challenges_dir = "challenges"
    
    if not os.path.exists(challenges_dir):
        console.print(f"[bold red]Challenges directory not found at {challenges_dir}[/bold red]")
        return False
    
    # Walk through all subdirectories to find challenge.yaml files
    for root, dirs, files in os.walk(challenges_dir):
        if "challenge.yaml" in files:
            challenge_files.append(os.path.join(root, "challenge.yaml"))
    
    if not challenge_files:
        console.print("[bold red]No challenge files found![/bold red]")
        return False
    
    console.print(f"[bold]Found {len(challenge_files)} challenge files[/bold]")
    
    # Sort challenge files for consistent ordering
    challenge_files.sort()
    
    # Test each challenge file
    success_count = 0
    for challenge_file in challenge_files:
        console.print(f"\n[bold]Testing: {challenge_file}[/bold]")
        try:
            with open(challenge_file, 'r') as file:
                import yaml
                challenge = yaml.safe_load(file)
                challenge['file_path'] = challenge_file
                challenge['dir'] = os.path.dirname(challenge_file)
            
            # Validate the challenge definition
            missing_fields = challenge_loader_module.validate_challenge(challenge)
            if missing_fields:
                console.print(f"[bold red]Challenge definition is invalid: {challenge_file}[/bold red]")
                for field in missing_fields:
                    console.print(f"[bold red]- Missing field: {field}[/bold red]")
                continue
            
            # Test database setup and solution
            try:
                conn = db_module.connect_to_db()
                
                if not db_module.setup_challenge_database(conn, challenge):
                    console.print(f"[bold red]Failed to set up database for: {challenge_file}[/bold red]")
                    continue
                
                # If solution file exists, test it
                validation = challenge.get('challenge', {}).get('validation', {})
                if validation.get('type') == 'result_set':
                    solution_file = os.path.join(challenge['dir'], validation.get('file'))
                    if os.path.exists(solution_file):
                        success, message = validator_module.validate_solution_file(solution_file, challenge, conn, db_module)
                        if not success:
                            console.print(f"[bold red]Solution validation failed for {challenge_file}: {message}[/bold red]")
                            continue
                    else:
                        console.print(f"[bold red]Solution file does not exist: {solution_file}[/bold red]")
                        continue
                
                console.print(f"[bold green]✓ Challenge passed: {challenge.get('title')}[/bold green]")
                success_count += 1
                
            except Exception as e:
                console.print(f"[bold red]Error testing challenge {challenge_file}: {e}[/bold red]")
                continue
            finally:
                if 'conn' in locals() and conn:
                    conn.close()
                    
        except Exception as e:
            console.print(f"[bold red]Error loading challenge {challenge_file}: {e}[/bold red]")
    
    # Print summary
    if success_count == len(challenge_files):
        console.print(f"\n[bold green]All {success_count}/{len(challenge_files)} challenges passed successfully![/bold green]")
        return True
    else:
        console.print(f"\n[bold yellow]{success_count}/{len(challenge_files)} challenges passed. Some challenges have issues.[/bold yellow]")
        return False
