"""High-level game orchestrator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from rich import print

from .round import Round

__all__ = ["Game"]


class Game:
    """Full multi-round Carioca match."""

    def __init__(self, *, players: int = 2, save_path: Path | None = None):
        self.players = players
        self.current_round = 1
        self.scores: List[int] = [0] * players
        self.save_path = save_path or Path("carioca_save.json")

    # ---------------------------------------------------------------------
    def play_round(self) -> None:
        rnd = Round(self.current_round)
        rnd.start(self.players, cards_each=(5 + self.current_round))
        print(
            f"[bold]Round {self.current_round} started with {self.players} players[/bold]"
        )
        current = 0
        while all(rnd.hands):
            hand = rnd.hands[current]
            hand.take(rnd.draw_pile.draw())
            rnd.discard_pile.append(hand.discard())
            if not hand:
                print(f"Player {current + 1} closed the round!")
                break
            current = (current + 1) % self.players
        for i, hand in enumerate(rnd.hands):
            self.scores[i] += sum(c.value for c in hand)
        self.current_round += 1

    def save(self) -> None:
        data = {"current_round": self.current_round, "scores": self.scores}
        self.save_path.write_text(json.dumps(data))

    def load(self) -> None:
        if self.save_path.exists():
            data = json.loads(self.save_path.read_text())
            self.current_round = data["current_round"]
            self.scores = data["scores"]
