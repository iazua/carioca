export interface Card {
  rank: string;
  suit: string | null;
  owner?: number;
  id?: string;
}

export type Zone = 'player_hand' | 'table_meld' | 'discard' | 'stock';

export interface Position {
  x: number;
  y: number;
}

export interface GameState {
  players: { id: number; name?: string; hand: Card[] }[];
  table_melds: { owner: number; cards: Card[] }[];
  discard_top: Card | null;
  stock_count: number;
  current_turn: number;
  phase: 'draw' | 'play' | 'end';
}

export interface MovePayload {
  type: 'move' | 'draw' | 'discard' | 'lay' | 'end_turn';
  data: any;
}
