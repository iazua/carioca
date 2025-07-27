import pytest

from carioca.deck import Deck


def test_deck_size() -> None:
    deck = Deck(seed=42)
    assert len(deck) == 108
    # drawing all should exhaust
    for _ in range(108):
        deck.draw()
    with pytest.raises(IndexError):
        deck.draw()
