from __future__ import annotations

import random
from collections import deque
from typing import Deque, Iterable, List

from .cards import Card, RANKS, Suit, JOKER

__all__ = ["Deck"]


class Deck:
    """A shoe with two 54-card decks (108 cards)."""

    def __init__(self, *, seed: int | None = None):
        self._rng = random.Random(seed)
        self._cards: Deque[Card] = deque(self._generate())
        self.shuffle()

    # Internal helpers --------------------------------------------------------
    def _generate(self) -> Iterable[Card]:
        for _ in range(2):  # two decks
            for rank in RANKS:
                for suit in Suit:  # type: ignore[misc]
                    if suit is Suit.JOKER:
                        break
                    yield Card(rank, suit)
            for _ in range(2):  # two Jokers per deck
                yield Card(JOKER)

    # Public API --------------------------------------------------------------
    def shuffle(self) -> None:
        cards: List[Card] = list(self._cards)
        self._rng.shuffle(cards)
        self._cards = deque(cards)

    def draw(self) -> Card:
        if not self._cards:
            raise IndexError("Deck is empty")
        return self._cards.popleft()

    def __len__(self) -> int:  # pragma: no cover
        return len(self._cards)
