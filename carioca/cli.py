"""Typer-powered command-line interface."""

from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from .game import Game

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def play(players: int = typer.Option(2, help="Number of players (2–4)")) -> None:
    """Start a fresh Carioca match."""
    game = Game(players=players)
    game.play_round()


@app.command()
def resume(save: Path = typer.Option(Path("carioca_save.json"), exists=True)) -> None:
    """Resume a saved game."""
    game = Game(save_path=save)
    game.load()
    print(f"Resuming from round {game.current_round}")
    game.play_round()


@app.command()
def score() -> None:
    """Show current leaderboard (stub)."""
    print("(scoreboard coming soon)")
