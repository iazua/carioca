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

## Features
* Full game engine with flexible YAML rules.
* Rich-styled Typer CLI.
* ≥90 % test coverage goal (pytest + coverage).
* Docker & GitHub Actions CI.

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

## Backend API

A minimal FastAPI server provides WebSocket rooms for multiplayer experiments.

```bash
poetry run uvicorn backend.app:app --reload
```

Connect clients to `ws://localhost:8000/ws/{room_id}` and broadcast game
messages as JSON.
