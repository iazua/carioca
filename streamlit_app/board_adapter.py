from __future__ import annotations

from typing import Any, Dict, List

from carioca.gamestate import GameState
from carioca.cards import Card
from carioca.hand import Hand

__all__ = ["to_component_state", "apply_move"]


def _card_to_dict(card: Card) -> Dict[str, Any]:
    return {"rank": card.rank, "suit": card.suit.value if card.suit else None}


def to_component_state(game: GameState) -> Dict[str, Any]:
    """Convert :class:`GameState` to the frontend representation."""

    players = [
        {"id": i, "hand": [_card_to_dict(c) for c in hand]}
        for i, hand in enumerate(game.round.hands)
    ]
    table_melds: List[Dict[str, Any]] = []
    for owner, melds in game.melds.items():
        for meld in melds:
            table_melds.append(
                {"owner": owner, "cards": [_card_to_dict(c) for c in meld]}
            )

    discard_top = (
        _card_to_dict(game.round.discard_pile[-1])
        if game.round.discard_pile
        else None
    )
    return {
        "players": players,
        "table_melds": table_melds,
        "discard_top": discard_top,
        "stock_count": len(game.round.draw_pile),
        "current_turn": game.current_player,
        "phase": "play",
    }


def apply_move(game: GameState, payload: Dict[str, Any]) -> None:
    """Apply a move payload returned by the frontend component."""

    move_type = payload.get("type")
    data = payload.get("data", {})

    if move_type == "draw":
        source = data.get("from")
        game.draw(from_discard=source == "discard")

    elif move_type == "discard":
        idx = int(data.get("card_id", 0))
        game.discard(idx)
        game.next_player()

    elif move_type == "lay":
        ids = [int(i) for i in data.get("card_ids", [])]
        game.meld(ids)

    elif move_type == "reorder":
        start = int(data.get("from", 0))
        end = int(data.get("to", 0))
        hand: Hand = game.hand
        card = hand.pop(start)
        hand.insert(end, card)

    elif move_type == "move":
        # Not yet implemented - ignore for now
        pass

