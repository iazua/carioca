from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional

try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:  # pragma: no cover - allow tests without deps
    Environment = None  # type: ignore
    FileSystemLoader = None  # type: ignore

from carioca.cards import Card, JOKER, Suit

if Environment:
    TEMPLATES = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))
else:  # pragma: no cover - tests without jinja2
    TEMPLATES = None


def card_svg(card: Optional[Card] = None, *, back: bool = False) -> str:
    """Return SVG for card as data URI."""
    if TEMPLATES is None:
        # Fallback minimal SVG for tests without Jinja2
        label = "?" if card is None else f"{card.rank}{card.suit or ''}"
        svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='160' height='240'><text x='10' y='20'>{label}</text></svg>"
    else:
        if back or card is None:
            tpl = TEMPLATES.get_template("card_back.svg")
            svg = tpl.render()
        else:
            rank = card.rank if card.rank != JOKER else "🃏"
            suit = card.suit.value if card.suit else ""
            color = "#d00" if card.suit in (Suit.HEARTS, Suit.DIAMONDS) else "#000"
            tpl = TEMPLATES.get_template("card_front.svg")
            svg = tpl.render(rank=rank, suit=suit, color=color)
    data = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{data}"
