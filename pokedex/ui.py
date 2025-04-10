"""
UI components for Pokemon SQL Trainer
"""

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box

console = Console()

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

def show_challenge(challenge, conn, db_module):
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
    schema = db_module.get_database_schema(conn)
    
    for table_name, columns in schema.items():
        console.print(f"\n[bold]{table_name}[/bold]")
        for column, dtype in columns:
            console.print(f"  - {column} ({dtype})")

def show_table_data(conn, db_module):
    """Display the data of a selected table."""
    tables = db_module.get_table_list(conn)
    
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
        
        columns, results = db_module.get_table_data(conn, selected_table)
        
        console.print(f"\n[bold]Data from table '{selected_table}':[/bold]")
        display_table(columns, results)
        
        if len(results) == 100:
            console.print("[yellow]Note: Only showing first 100 rows.[/yellow]")
            
    except ValueError:
        console.print("[bold red]Invalid input. Please enter a number.[/bold red]")

def show_hints(hints):
    """Display hints for the current challenge."""
    if hints:
        console.print("\n[bold yellow]Pokedex Hints:[/bold yellow]")
        for i, hint in enumerate(hints, 1):
            console.print(f"[yellow]{i}. {hint}[/yellow]")
    else:
        console.print("[yellow]No hints available for this challenge.[/yellow]")
