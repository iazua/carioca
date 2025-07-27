from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:  # pragma: no cover - optional in tests
    import streamlit as st  # type: ignore
    from streamlit.components.v1 import declare_component
except ModuleNotFoundError:  # pragma: no cover - allow tests without streamlit
    st = None  # type: ignore
    declare_component = lambda *a, **k: lambda **_kwargs: None  # type: ignore

_COMPONENT_NAME = "carioca_component"
_BUILD_DIR = Path(__file__).parent / ".." / "frontend" / "build"

_carioca_component = declare_component(_COMPONENT_NAME, path=str(_BUILD_DIR))


def carioca_component(game_state: dict[str, Any], key: str | None = None) -> dict[str, Any]:
    """Render the Carioca board and return updated state."""
    data = _carioca_component(game_state=game_state, key=key)
    if data is None:
        return game_state
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            pass
    if isinstance(data, dict):
        return data
    return game_state
