"""
Challenge execution logic
"""

import os
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

console = Console()
sql_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'GROUP BY', 
                'ORDER BY', 'HAVING', 'LIMIT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 
                'ALTER', 'DROP', 'AND', 'OR', 'NOT', 'IN', 'BETWEEN', 'LIKE', 'IS NULL',
                'IS NOT NULL', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'AS', 'DISTINCT', 'UNION']

# Create style for prompt
prompt_style = Style.from_dict({
    'prompt': '#00aa00 bold',
    'continuation': '#aaaa00 italic',
})

def get_user_input(session, prompt_text="SQL> "):
    """Get multiline input from user with enhanced prompt features."""
    try:
        return session.prompt(prompt_text, multiline=False, 
                             auto_suggest=AutoSuggestFromHistory(),
                             style=prompt_style)
    except KeyboardInterrupt:
        return "q"  # Return quit command on Ctrl+C
    except EOFError:
        return "q"  # Return quit command on Ctrl+D

def interactive_mode(challenge_num=None, db_module=None, ui_module=None, 
                     validator_module=None, challenge_loader_module=None):
    """Run the challenge interface in interactive mode."""
    # Create prompt session with history
    sql_completer = WordCompleter(sql_keywords, ignore_case=True)
    session = PromptSession(history=InMemoryHistory(), completer=sql_completer)
    
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
        # Show challenge list grouped by difficulty
        console.print("[bold]Available Pokemon SQL Challenges:[/bold]")
        
        # Group challenges by difficulty
        beginner_challenges = []
        intermediate_challenges = []
        advanced_challenges = []
        
        for i, challenge in enumerate(challenges, 1):
            difficulty = challenge.get('difficulty', '').lower()
            if difficulty == 'beginner':
                beginner_challenges.append((i, challenge))
            elif difficulty == 'intermediate':
                intermediate_challenges.append((i, challenge))
            elif difficulty == 'advanced':
                advanced_challenges.append((i, challenge))
            else:
                # For challenges with unknown difficulty
                beginner_challenges.append((i, challenge))
        
        # Display challenges by difficulty groups
        if beginner_challenges:
            console.print("\n[bold green]Beginner Challenges:[/bold green]")
            for i, challenge in beginner_challenges:
                console.print(f"{i}. {challenge.get('title')}")
        
        if intermediate_challenges:
            console.print("\n[bold yellow]Intermediate Challenges:[/bold yellow]")
            for i, challenge in intermediate_challenges:
                console.print(f"{i}. {challenge.get('title')}")
        
        if advanced_challenges:
            console.print("\n[bold red]Advanced Challenges:[/bold red]")
            for i, challenge in advanced_challenges:
                console.print(f"{i}. {challenge.get('title')}")
            
        # Ask user to select a challenge
        console.print("\nEnter the number of the challenge you want to try (or 'q' to quit):")
        selection = get_user_input(session, "> ")
        
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
            
            # Enhanced multiline input collection
            while True:
                multiline_prompt = "SQL> " if not lines else "...> "
                line = get_user_input(session, multiline_prompt)
                
                # Handle single-letter commands immediately - no semicolon required
                if not lines and line.lower() in ['q', 'h', 'v']:
                    user_sql = line.lower()
                    break
                    
                lines.append(line)
                user_sql = "\n".join(lines)
                
                # If line contains semicolon, we can execute the SQL
                if ';' in line:
                    break
                    
            if user_sql == 'q':
                break
                
            if user_sql == 'v':
                ui_module.show_table_data(conn, db_module)
                get_user_input(session, "\nPress Enter to continue...")
                continue
                
            if user_sql == 'h':
                hints = challenge.get('challenge', {}).get('hints', [])
                ui_module.show_hints(hints)
                get_user_input(session, "\nPress Enter to continue...")
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
                                get_user_input(session, "")
                                current_challenge += 1
                                challenge = challenges[current_challenge]
                                db_module.setup_challenge_database(conn, challenge)
                                continue
                            else:
                                console.print("\n[bold green]╔══════════════════════════════════════════════════════════════╗[/bold green]")
                                console.print("[bold green]║                   [bold yellow]✨  CONGRATULATIONS!  ✨[/bold yellow]                   ║[/bold green]")
                                console.print("[bold green]║                                                              ║[/bold green]")
                                console.print("[bold green]║[/bold green]  [bold cyan]You've mastered all Pokémon SQL challenges![/bold cyan]  [bold green]               ║[/bold green]")
                                console.print("[bold green]║[/bold green]  [bold magenta]Professor Oak would be proud of your database skills![/bold magenta]  [bold green]     ║[/bold green]")
                                console.print("[bold green]║                                                              ║[/bold green]")
                                console.print("[bold green]║[/bold green]  [bold yellow]🏆 You are now officially a POKÉMON SQL MASTER! 🏆[/bold yellow]  [bold green]        ║[/bold green]")
                                console.print("[bold green]╚══════════════════════════════════════════════════════════════╝[/bold green]")
                        else:
                            console.print(f"[bold red]{message}[/bold red]")
                except Exception as e:
                    console.print(f"[bold red]Error: {e}[/bold red]")
                    
            get_user_input(session, "\nPress Enter to continue...")
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
