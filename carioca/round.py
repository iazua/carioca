from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .cards import Card
from .deck import Deck
from .hand import Hand

__all__ = ["Round"]


@dataclass
class Round:
    """Single Carioca round."""

    number: int
    draw_pile: Deck = field(default_factory=Deck)
    discard_pile: List[Card] = field(default_factory=list)
    hands: List[Hand] = field(default_factory=list)

    def start(self, players: int, cards_each: int) -> None:
        self.hands = [Hand() for _ in range(players)]
        for _ in range(cards_each):
            for hand in self.hands:
                hand.take(self.draw_pile.draw())
        self.discard_pile.append(self.draw_pile.draw())

    # Minimal public helpers --------------------------------------------------
    def top_discard(self) -> Card:
        return self.discard_pile[-1]

    def can_close(self, hand: Hand, requirement: str) -> bool:
        """Check if hand satisfies the round requirement (very naive)."""
        # For demo we just allow closure when empty; full logic T.B.D.
        return not hand
