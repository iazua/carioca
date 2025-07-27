import { useState } from 'react';
import type { Card } from '../types';

export function useDrag() {
  const [dragging, setDragging] = useState<Card | null>(null);

  function onDragStart(card: Card) {
    setDragging(card);
  }

  function onDragEnd() {
    setDragging(null);
  }

  return { dragging, onDragStart, onDragEnd };
}
