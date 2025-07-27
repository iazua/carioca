from carioca.cards import Card, Suit
from carioca.hand import Hand


def test_hand_points() -> None:
    hand = Hand()
    hand.take(Card("5", Suit.HEARTS))
    hand.take(Card("A", Suit.CLUBS))
    hand.take(Card.from_str("🃏"))
    assert hand.points() == 5 + 20 + 30


def test_card_from_str() -> None:
    card = Card.from_str("Q" + str(Suit.SPADES))
    assert card.rank == "Q" and card.suit == Suit.SPADES
    assert Card.from_str("🃏").is_joker
