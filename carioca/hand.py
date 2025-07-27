from __future__ import annotations

try:
    from rich.console import Console
    from rich.table import Table
except ModuleNotFoundError:  # pragma: no cover - rich optional in tests
    Console = None
    Table = None

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

    def points(self) -> int:
        """Total value of all cards in hand."""
        return sum(c.value for c in self)

    # Pretty-print ------------------------------------------------------------
    def show(self, *, title: str | None = None) -> None:  # pragma: no cover
        if Console is None or Table is None:
            raise RuntimeError("rich package required for show()")
        table = Table(title=title, show_header=False)
        table.add_row(" ".join(map(str, self)))
        Console().print(table)
