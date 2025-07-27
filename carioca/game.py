"""High-level game orchestrator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

try:
    from rich import print
except ModuleNotFoundError:  # pragma: no cover - tests without rich
    print = __builtins__["print"]

from .gamestate import GameState
__all__ = ["Game"]


class Game:
    """Full multi-round Carioca match."""

    def __init__(self, *, players: int = 2, save_path: Path | None = None, total_rounds: int = 8):
        self.players = players
        self.total_rounds = total_rounds
        self.save_path = save_path or Path("carioca_save.json")
        self.state: GameState = GameState.new(players, total_rounds)

    # ------------------------------------------------------------------
    @property
    def current_round(self) -> int:
        return self.state.round.number

    @property
    def scores(self) -> List[int]:
        return self.state.scores

    # ------------------------------------------------------------------
    def play_round(self) -> None:
        rnd = self.state.round
        print(
            f"[bold]Round {rnd.number} started with {self.players} players[/bold]"
        )
        while True:
            player = self.state.current_player
            print(f"-- Turn of player {player + 1} --")
            self.state.draw()
            discarded = self.state.discard(-1)
            print(f"Player {player + 1} discarded {discarded}")
            if self.state.can_close() or len(self.state.round.draw_pile) == 0:
                print(f"Player {player + 1} closes the round")
                self.state.close_round()
                self.save()
                break
            self.state.next_player()
            self.save()
            if self.state.round.number != rnd.number:
                break

    # ------------------------------------------------------------------
    def save(self) -> None:
        data = self.state.to_dict()
        self.save_path.write_text(json.dumps(data))

    def load(self) -> None:
        if self.save_path.exists():
            data = json.loads(self.save_path.read_text())
            self.state = GameState.from_dict(data)
            self.players = len(self.state.scores)
            self.total_rounds = self.state.total_rounds
