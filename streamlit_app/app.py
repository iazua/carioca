from __future__ import annotations

import streamlit as st
from streamlit_lottie import st_lottie

# When this file is executed by Streamlit the module is run as a script and
# not as part of a package. Relative imports therefore fail because
# ``__package__`` is not set. Import the helpers using absolute paths so the
# application works both locally and when deployed on Streamlit Cloud.
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
selected = st.multiselect(
    "Selecciona cartas", options=list(range(len(game.hand))), format_func=lambda i: str(game.hand[i]), key="sel_cards"
)
cols = st.columns(len(game.hand))
for i, card in enumerate(game.hand):
    with cols[i]:
        st.image(card_svg(card), use_column_width=True)

if st.button("Descartar", key="discard_btn") and selected:
    game.discard(selected[0])
    game.next_player()
    st.session_state.sel_cards = []

if st.button("Formar trío/escala", key="meld_btn") and selected:
    if game.meld(selected):
        st.success("Combinación válida")
    else:
        st.error("No es trío ni escala")
    st.session_state.sel_cards = []

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
