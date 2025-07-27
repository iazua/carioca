from __future__ import annotations

from rich.console import Console
from rich.table import Table

from .cards import Card

__all__ = ["Hand"]


class Hand(list[Card]):
    """A player's hand."""

    def take(self, card: Card) -> None:
        self.append(card)
        self.sort()

    def discard(self, index: int = -1) -> Card:
        try:
            return self.pop(index)
        finally:
            self.sort()

    # Pretty-print ------------------------------------------------------------
    def show(self, *, title: str | None = None) -> None:  # pragma: no cover
        table = Table(title=title, show_header=False)
        table.add_row(" ".join(map(str, self)))
        Console().print(table)
