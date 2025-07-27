from carioca.cards import Card, Suit, JOKER


def test_card_value() -> None:
    assert Card("J", Suit.CLUBS).value == 10
    assert Card("A", Suit.HEARTS).value == 20
    assert Card(JOKER).is_joker
