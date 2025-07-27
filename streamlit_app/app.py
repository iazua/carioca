from __future__ import annotations

import streamlit as st
from streamlit_lottie import st_lottie

# When this file is executed by Streamlit the module is run as a script and
# not as part of a package. Relative imports therefore fail because
# ``__package__`` is not set. Import the helpers using absolute paths so the
# application works both locally and when deployed on Streamlit Cloud.
import os
import sys

# Ensure the carioca package can be imported when the app is executed
# directly by Streamlit. When running ``streamlit run streamlit_app/app.py``
# the working directory is the repo root but the script's directory is
# ``streamlit_app``. Insert the repository root into ``sys.path`` so that the
# ``carioca`` package is discoverable without requiring installation.
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, os.pardir))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from state import GameState
from utils import card_svg

st.set_page_config(page_title="Carioca", page_icon="🃏", layout="wide")

THEME = "dark"
BASE_COLOR = "#361860"
ACCENT = "#F1AC4B"

# -------------------------------------------------------------------
# Sidebar – new game setup
# -------------------------------------------------------------------
with st.sidebar:
    st.header("Nueva partida")
    players = st.slider("Jugadores", 2, 4, 2, key="players")
    rounds = st.slider("Rondas", 1, 8, 8, key="rounds")
    if st.button("Iniciar") or "game" not in st.session_state:
        st.session_state.game = GameState.new(players, rounds)
    st.markdown("[Reglas](https://example.com/reglas.pdf)")

# -------------------------------------------------------------------
# Main Header – title and scoreboard
# -------------------------------------------------------------------
if "game" not in st.session_state:
    st.session_state.game = GameState.new(players, rounds)

game: GameState = st.session_state.game

st.title(f"Carioca – Ronda {game.round.number}")
score_table = "| Jugador | Puntaje |\n|--------|---------|\n"
for i, s in enumerate(game.scores):
    score_table += f"| {i+1} | {s} |\n"
st.markdown(score_table)

# -------------------------------------------------------------------
# Board area – player's hand and piles
# -------------------------------------------------------------------
col_deck, col_discard = st.columns(2)
if col_deck.button("Robar mazo", key="draw_deck", help="D", use_container_width=True):
    game.draw(from_discard=False)
if col_discard.button(f"Robar pozo ({len(game.round.discard_pile)})", key="draw_discard", help="P", use_container_width=True):
    game.draw(from_discard=True)

st.subheader("Tu mano")
# Clear previous selection before rendering widget
if st.session_state.get("clear_sel_cards"):
    if "sel_cards" in st.session_state:
        st.session_state.sel_cards = []
    st.session_state.clear_sel_cards = False

selected = st.session_state.setdefault("sel_cards", [])
cols = st.columns(len(game.hand))
for i, card in enumerate(game.hand):
    btn_key = f"card_{i}"
    border = f"2px solid {ACCENT}" if i in selected else "1px solid transparent"
    st.markdown(
        f"""
        <style>
        div[data-testid="stButton"][key="{btn_key}"] > button {{
            background: url('{card_svg(card)}') no-repeat center center;
            background-size: contain;
            height: 240px;
            width: 100%;
            padding: 0;
            border: {border};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button(" ", key=btn_key):
        if i in selected:
            selected.remove(i)
        else:
            selected.append(i)
        st.session_state.sel_cards = selected
        st.experimental_rerun()

if st.button("Descartar", key="discard_btn") and selected:
    game.discard(selected[0])
    st.session_state.clear_sel_cards = True

if st.button("Formar trío/escala", key="meld_btn") and selected:
    if game.meld(selected):
        st.success("Combinación válida")
    else:
        st.error("No es trío ni escala")
    st.session_state.clear_sel_cards = True

# -------------------------------------------------------------------
# Meld area
# -------------------------------------------------------------------
for player, melds in game.melds.items():
    with st.expander(f"Jugador {player+1}"):
        for meld in melds:
            st.markdown(" ".join(f"{c}" for c in meld))

# -------------------------------------------------------------------
# Footer – log and close round
# -------------------------------------------------------------------
if st.button("Cerrar ronda", key="close_btn", help="C"):
    if game.can_close():
        game.close_round()
        st.success("Ronda cerrada")
        if game.round.number > game.total_rounds:
            st.balloons()
            winner = min(range(len(game.scores)), key=lambda i: game.scores[i])
            st.write(f"Ganador: Jugador {winner+1}")
    else:
        st.error("No puedes cerrar aún")
