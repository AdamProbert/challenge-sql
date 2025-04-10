#!/usr/bin/env python3.11
"""
Pokemon SQL Trainer - Command Line Interface
This script provides a command-line interface for users to interact with SQL learning challenges.
"""

import argparse
import os
import sys
import signal
import colorama
from rich.console import Console

# Import our modules
from pokedex import db, ui, validator, challenge_loader, challenge_runner

colorama.init()
console = Console()

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    console.print("\n[bold yellow]Exiting Pokemon SQL Trainer. Keep training to become a SQL Master![/bold yellow]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parse_args():
    parser = argparse.ArgumentParser(description='Pokemon SQL Trainer Challenge')
    parser.add_argument('--challenge', type=int, help='Specific challenge number to run')
    parser.add_argument('--test-challenge', metavar='FILE', help='Test a challenge YAML definition')
    parser.add_argument('--test-all', action='store_true', help='Test all challenge definitions')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.test_all:
        outcome = challenge_runner.test_all(
            db_module=db,
            ui_module=ui,
            validator_module=validator,
            challenge_loader_module=challenge_loader
        )
        if outcome == False:
            console.print("[bold red]Some challenges failed the test.[/bold red]")
            sys.exit(1)
    elif args.test_challenge:
        challenge_runner.test_challenge(
            args.test_challenge,
            db_module=db,
            ui_module=ui,
            validator_module=validator,
            challenge_loader_module=challenge_loader
        )
    else:
        challenge_runner.interactive_mode(
            args.challenge,
            db_module=db,
            ui_module=ui,
            validator_module=validator,
            challenge_loader_module=challenge_loader
        )

if __name__ == '__main__':
    main()
