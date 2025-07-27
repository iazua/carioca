from carioca.ai import choose_discard
from carioca.cards import Card, Suit
from carioca.hand import Hand


def test_choose_discard() -> None:
    hand = Hand([Card("2", Suit.CLUBS), Card("K", Suit.HEARTS)])
    assert choose_discard(hand) == 1

