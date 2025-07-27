from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

__all__ = ["Suit", "Card", "JOKER"]


class Suit(str, Enum):
    """Card suits including a pseudo-suit for Jokers."""

    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"
    JOKER = "🃏"  # handy when printing

    def __str__(self) -> str:  # pragma: no cover
        return self.value


VALUES: dict[str, int] = {
    **{str(n): n for n in range(2, 11)},
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 20,
    "JOKER": 30,
}
RANKS: list[str] = [*map(str, range(2, 11)), "J", "Q", "K", "A"]
JOKER = "JOKER"


@dataclass(frozen=True, slots=True)
class Card:
    """Immutable playing card."""

    rank: str
    suit: Suit | None = None  # None for Joker

    def __post_init__(self) -> None:
        if (self.rank == JOKER) != (self.suit is None):
            raise ValueError("Joker must have no suit and vice-versa")
        if self.rank not in VALUES:
            raise ValueError(f"Invalid rank: {self.rank}")

    # Useful dunder overloads -------------------------------------------------
    def __str__(self) -> str:  # pragma: no cover
        return self.rank if self.is_joker else f"{self.rank}{self.suit}"

    def __lt__(self, other: "Card") -> bool:  # ordering for sorting scales
        return (self.value, self.rank) < (other.value, other.rank)

    # Convenience properties --------------------------------------------------
    @property
    def is_joker(self) -> bool:
        return self.rank == JOKER

    @property
    def value(self) -> int:
        return VALUES[self.rank]
