"""
Challenge loading and validation utilities
"""

import os
import yaml
from rich.console import Console

console = Console()

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

def validate_challenge(challenge):
    """Validate that a challenge definition has all required fields."""
    required_fields = [
        'title', 'description', 'difficulty', 'setup', 
        'challenge.task', 'challenge.validation'
    ]
    
    missing_fields = []
    
    for field in required_fields:
        parts = field.split('.')
        obj = challenge
        for part in parts:
            if isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                missing_fields.append(field)
                break
    
    # Validate setup files exist
    for setup_file in challenge.get('setup', []):
        file_path = os.path.join(challenge['dir'], setup_file.get('file'))
        if not os.path.exists(file_path):
            missing_fields.append(f"setup file: {setup_file.get('file')}")
    
    # Validate solution file exists if result_set validation
    validation = challenge.get('challenge', {}).get('validation', {})
    if validation.get('type') == 'result_set':
        solution_file = os.path.join(challenge['dir'], validation.get('file'))
        if not os.path.exists(solution_file):
            missing_fields.append(f"solution file: {validation.get('file')}")
    
    return missing_fields
