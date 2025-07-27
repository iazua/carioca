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
# Game setup – previously sidebar
# -------------------------------------------------------------------
with st.expander("Nueva partida", expanded=False):
    players = st.slider("Jugadores", 2, 4, 2, key="players_setup")
    rounds = st.slider("Rondas", 1, 8, 8, key="rounds_setup")
    start = st.button("Iniciar")

if "game" not in st.session_state or start:
    st.session_state.game = GameState.new(players, rounds)
st.markdown("[Reglas](https://example.com/reglas.pdf)")

# -------------------------------------------------------------------
# Main Header – title and scoreboard
# -------------------------------------------------------------------
if "game" not in st.session_state:
    st.session_state.game = GameState.new(players, rounds)

game: GameState = st.session_state.game

st.title(f"Carioca – Ronda {game.round.number}")

scores_data = [
    {"Jugador": f"➡️ {i+1}" if i == game.current_player else i + 1, "Puntaje": s}
    for i, s in enumerate(game.scores)
]
st.table(scores_data)

if st.session_state.pop("show_balloons", False):
    st.balloons()
if "round_msg" in st.session_state:
    st.success(st.session_state.pop("round_msg"))

# -------------------------------------------------------------------
# Board area – player's hand and piles
# -------------------------------------------------------------------
col_deck, col_discard = st.columns(2)
if col_deck.button("Robar mazo", key="draw_deck", help="D", use_container_width=True):
    game.draw(from_discard=False)
if col_discard.button(
    f"Robar pozo ({len(game.round.discard_pile)})",
    key="draw_discard",
    help="P",
    use_container_width=True,
):
    game.draw(from_discard=True)

st.subheader("Tu mano")
# Clear previous selection before rendering widget
if st.session_state.get("clear_sel_cards"):
    if "sel_cards" in st.session_state:
        st.session_state.sel_cards = []
    st.session_state.clear_sel_cards = False

selected = st.session_state.get("sel_cards", [])
cols = st.columns(len(game.hand))
for i, card in enumerate(game.hand):
    with cols[i]:
        st.image(card_svg(card), use_column_width=True)
        chosen = st.toggle("", key=f"card_{i}", value=i in selected)
        if chosen and i not in selected:
            selected.append(i)
        if not chosen and i in selected:
            selected.remove(i)
selected.sort()
st.session_state.sel_cards = selected

if st.button("Descartar", key="discard_btn") and selected:
    game.discard(selected[0])
    game.next_player()
    st.session_state.clear_sel_cards = True
    st.experimental_rerun()

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
        st.session_state.round_msg = "Ronda cerrada"
        if game.round.number > game.total_rounds:
            st.session_state.show_balloons = True
            winner = min(range(len(game.scores)), key=lambda i: game.scores[i])
            st.session_state.round_msg += f" – Ganador: Jugador {winner+1}"
        st.experimental_rerun()
    else:
        st.error("No puedes cerrar aún")
