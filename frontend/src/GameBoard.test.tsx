import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import { GameBoard } from './GameBoard';
import type { GameState } from './types';

const state: GameState = {
  players: [{ id: 1, hand: [{ rank: 'A', suit: '♠', id: 'c1' }] }],
  table_melds: [],
  discard_top: null,
  stock_count: 10,
  current_turn: 0,
  phase: 'draw',
};

describe('GameBoard', () => {
  it('renders hand', () => {
    const onMove = vi.fn();
    const { getByRole } = render(<GameBoard state={state} onMove={onMove} />);
    expect(getByRole('img')).toBeTruthy();
  });
});
