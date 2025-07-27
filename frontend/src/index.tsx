import React from 'react';
import ReactDOM from 'react-dom/client';
import { GameBoard } from './GameBoard';
import type { GameState, MovePayload } from './types';

declare global {
  interface Window {
    Streamlit?: any;
  }
}

function mount() {
  const root = ReactDOM.createRoot(document.getElementById('root')!);
  const args = window.parent?.Streamlit?.args ?? {};
  const state: GameState = args.game_state;

  function onMove(payload: MovePayload) {
    if (window.Streamlit) {
      window.Streamlit.setComponentValue(payload);
    }
  }

  root.render(<GameBoard state={state} onMove={onMove} />);
}

if (document.readyState !== 'loading') {
  mount();
} else {
  document.addEventListener('DOMContentLoaded', mount);
}

export default GameBoard;
