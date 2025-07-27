# Carioca – Chilean Card Game (Python)

Play **Carioca** right from your terminal:

```bash
poetry install
poetry run carioca play --players 3
```

Launch the Streamlit UI:

```bash
poetry run streamlit run streamlit_app/app.py
```

### Multiplayer backend (experimental)

An optional FastAPI server provides simple WebSocket rooms used to
synchronise state between browser clients. Start it locally with:

```bash
python backend/main.py
```

The Streamlit app can connect using `st.experimental_connection` and the
WebSocket URL `ws://localhost:8000/ws/<room>`.

## Features
* Full game engine with flexible YAML rules.
* Rich-styled Typer CLI.
* ≥90 % test coverage goal (pytest + coverage).
* Docker & GitHub Actions CI.
* Experimental AI helpers for automated opponents.

See `docs/` soon for detailed rules.

## Streamlit Component
A minimal interactive board is implemented as a Streamlit component.

Build the frontend:

```bash
cd frontend
npm install
npm run build
```

Run the example app:

```bash
poetry run streamlit run example_app.py
```
