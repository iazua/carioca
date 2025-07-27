from streamlit_app.board_adapter import to_component_state, apply_move
from carioca.gamestate import GameState
from carioca.cards import Card, Suit
from carioca.hand import Hand


def test_to_component_state_keys() -> None:
    game = GameState.new(players=2)
    state = to_component_state(game)
    assert state["current_turn"] == game.current_player
    assert state["stock_count"] == len(game.round.draw_pile)
    assert len(state["players"]) == 2


def test_apply_move_draw_discard() -> None:
    game = GameState.new(players=2)
    initial = len(game.hand)
    apply_move(game, {"type": "draw", "data": {"from": "stock"}})
    assert len(game.hand) == initial + 1
    apply_move(game, {"type": "discard", "data": {"card_id": 0}})
    assert len(game.round.discard_pile) == 2


def test_apply_move_reorder() -> None:
    game = GameState.new(players=1)
    game.round.hands[0] = Hand([Card("3", Suit.SPADES), Card("4", Suit.SPADES)])
    apply_move(game, {"type": "reorder", "data": {"from": 0, "to": 1}})
    assert game.round.hands[0][1].rank == "3"


def test_apply_move_lay_trio() -> None:
    game = GameState.new(players=1)
    game.round.hands[0] = Hand([
        Card("2", Suit.CLUBS),
        Card("2", Suit.DIAMONDS),
        Card("2", Suit.HEARTS),
    ])
    apply_move(game, {"type": "lay", "data": {"card_ids": [0, 1, 2]}})
    assert len(game.round.hands[0]) == 0
    assert game.melds[0]

