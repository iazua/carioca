from __future__ import annotations

import streamlit as st
import time

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

from state import GameState  # noqa: E402
from python.carioca_component import carioca_component  # noqa: E402
from board_adapter import to_component_state, apply_move  # noqa: E402

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

with st.expander("Reglas y opciones", expanded=False):
    st.markdown(
        """
        - Roba cartas del mazo o pozo en tu turno.
        - Forma tríos o escaleras para bajar tus cartas.
        - Cuando estés listo, descarta y cierra la ronda.
        """
    )
    st.markdown("[Reglamento completo](https://example.com/reglas.pdf)")
    st.toggle("Auto-refrescar puntaje", key="auto_refresh_scores")

if "game" not in st.session_state or start:
    st.session_state.game = GameState.new(players, rounds)

# -------------------------------------------------------------------
# Main Header – title and scoreboard
# -------------------------------------------------------------------
if "game" not in st.session_state:
    st.session_state.game = GameState.new(players, rounds)

game: GameState = st.session_state.game

st.title(f"Carioca – Ronda {game.round.number}")
st.subheader("Puntajes")
scores_placeholder = st.empty()


def render_scores() -> None:
    scores_data = [
        {"Jugador": f"➡️ {i+1}" if i == game.current_player else i + 1, "Puntaje": s}
        for i, s in enumerate(game.scores)
    ]
    scores_placeholder.table(scores_data)


render_scores()

if st.session_state.get("auto_refresh_scores"):
    time.sleep(5)
    st.experimental_rerun()

if st.session_state.pop("show_balloons", False):
    st.balloons()
if "round_msg" in st.session_state:
    st.success(st.session_state.pop("round_msg"))

# -------------------------------------------------------------------
# Board area – player's hand and piles
# -------------------------------------------------------------------
state_dict = to_component_state(game)
payload = carioca_component(state_dict, key="board")
if isinstance(payload, dict) and payload.get("type"):
    apply_move(game, payload)
    st.experimental_rerun()

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
