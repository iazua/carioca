from streamlit_app.utils import card_svg
from carioca.cards import Card, Suit


def test_card_svg() -> None:
    svg_data = card_svg(Card("A", Suit.SPADES))
    assert svg_data.startswith("data:image/svg+xml;base64,")
