from __future__ import annotations

import streamlit as st

from carioca.gamestate import GameState
from python.carioca_component import carioca_component

st.set_page_config(page_title="Carioca Component")

if "game" not in st.session_state:
    st.session_state.game = GameState.new(players=2)

game: GameState = st.session_state.game

state_dict = game.to_dict()
updated = carioca_component(state_dict, key="carioca")

if updated != state_dict:
    st.session_state.game = GameState.from_dict(updated)
    game = st.session_state.game

st.json(game.to_dict())
