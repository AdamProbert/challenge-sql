"""Challenge loading and validation utilities."""

from __future__ import annotations

import yaml
from pathlib import Path
from rich.console import Console

console = Console()

BASE_DIR = Path(__file__).resolve().parent.parent
CHALLENGES_ROOT = BASE_DIR / "challenges"


def validate_challenge_directories(difficulty: str) -> bool:
    """Validate that challenge directories are sequentially numbered."""
    challenge_dir = CHALLENGES_ROOT / difficulty
    if not challenge_dir.exists():
        return True
    
    numbered_dirs = []
    for entry in challenge_dir.iterdir():
        if entry.is_dir() and entry.name.isdigit():
            numbered_dirs.append(int(entry.name))
    
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

def load_challenges() -> list[dict]:
    """Load all challenge definitions from YAML files in numbered directories."""
    challenges = []
    
    for difficulty in ["beginner", "intermediate", "advanced"]:
        # Validate directory structure
        validate_challenge_directories(difficulty)
        
        challenge_dir = CHALLENGES_ROOT / difficulty
        if not challenge_dir.exists():
            continue
            
        subdirs = []
        for entry in challenge_dir.iterdir():
            if entry.is_dir() and entry.name.isdigit():
                subdirs.append((int(entry.name), entry))
                
        # Sort directories by number
        subdirs.sort(key=lambda item: item[0])
        
        # Load challenge from each directory
        for _, dir_path in subdirs:
            challenge_file = dir_path / "challenge.yaml"
            
            if challenge_file.exists():
                try:
                    with challenge_file.open("r", encoding="utf-8") as file:
                        challenge = yaml.safe_load(file)
                        challenge["file_path"] = str(challenge_file)
                        challenge["dir"] = str(dir_path)
                        challenges.append(challenge)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not load challenge {challenge_file}: {e}[/yellow]")
    
    # Sort by difficulty
    difficulty_order = {"beginner": 1, "intermediate": 2, "advanced": 3}
    challenges.sort(key=lambda x: difficulty_order.get(x.get("difficulty"), 999))
    return challenges

def _challenge_dir(challenge: dict) -> Path:
    return Path(challenge["dir"]).resolve()


def validate_challenge(challenge: dict) -> list[str]:
    """Validate that a challenge definition has all required fields."""
    required_fields = [
        "title",
        "description",
        "difficulty",
        "setup",
        "challenge.task",
        "challenge.validation",
    ]
    
    missing_fields = []
    
    for field in required_fields:
        parts = field.split(".")
        obj = challenge
        for part in parts:
            if isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                missing_fields.append(field)
                break
    
    # Validate setup files exist
    challenge_dir = _challenge_dir(challenge)
    for setup_file in challenge.get("setup", []):
        file_path = challenge_dir / setup_file.get("file")
        if not file_path.exists():
            missing_fields.append(f"setup file: {setup_file.get('file')}")
    
    # Validate solution file exists if result_set validation
    validation = challenge.get("challenge", {}).get("validation", {})
    if validation.get("type") == "result_set":
        solution_file = challenge_dir / validation.get("file")
        if not solution_file.exists():
            missing_fields.append(f"solution file: {validation.get('file')}")
    
    return missing_fields
