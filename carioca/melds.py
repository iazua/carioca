"""Helpers to detect valid trios and scales according to Carioca rules."""

from __future__ import annotations

from typing import Iterable, List

from .cards import Card

__all__ = ["is_trio", "is_scale"]


def is_trio(cards: Iterable[Card]) -> bool:
    """Return True iff cards form a (possibly wild) trio."""
    cs: List[Card] = sorted(cards)
    if len(cs) != 3:
        return False
    ranks = {c.rank for c in cs if not c.is_joker}
    jokers = sum(c.is_joker for c in cs)
    return len(ranks) == 1 and jokers <= 1


def is_scale(cards: Iterable[Card]) -> bool:
    """Return True iff cards form a valid scale (run) with ≤1 Joker."""
    cs: List[Card] = sorted(cards)
    if len(cs) < 4:
        return False
    suits = {c.suit for c in cs if not c.is_joker}
    if len(suits) != 1:
        return False
    jokers = sum(c.is_joker for c in cs)
    if jokers > 1:
        return False
    # Remove jokers for sequence check
    seq = [c for c in cs if not c.is_joker]
    # Consecutive values?
    return all(seq[i + 1].value - seq[i].value == 1 for i in range(len(seq) - 1))
