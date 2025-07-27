"""Basic AI helpers for Carioca."""

from __future__ import annotations
from typing import Sequence
from ..cards import Card

__all__ = ["choose_discard"]


def choose_discard(hand: Sequence[Card]) -> int:
    """Return index of card to discard from *hand*.

    This naive strategy discards the highest value card.
    """
    if not hand:
        return -1
    idx, _ = max(enumerate(hand), key=lambda pair: pair[1].value)
    return idx

