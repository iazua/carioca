import React from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { motion } from 'framer-motion';
import { Card, GameState, MovePayload } from './types';
import { useDrag } from './hooks/useDrag';

export interface GameBoardProps {
  state: GameState;
  onMove: (payload: MovePayload) => void;
}

export function GameBoard({ state, onMove }: GameBoardProps) {
  const { onDragStart, onDragEnd } = useDrag();

  function handleDragEnd(result: any) {
    onDragEnd();
    if (!result.destination) return;
    const cardId = result.draggableId;
    onMove({
      type: 'move',
      data: {
        card_ids: [cardId],
        source_zone: result.source.droppableId,
        target_zone: result.destination.droppableId,
      },
    });
  }

  return (
    <DragDropContext onDragEnd={handleDragEnd} onDragStart={(e) => onDragStart(e.source)}>
      <div style={{ display: 'flex', flexDirection: 'row', gap: '1rem' }}>
        <Droppable droppableId="player_hand" direction="horizontal">
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              style={{
                display: 'flex',
                background: snapshot.isDraggingOver ? '#f0f0f0' : 'transparent',
                transition: 'background 0.2s ease',
              }}
            >
              {state.players[0].hand.map((c: Card, idx: number) => (
                <Draggable draggableId={`${idx}`} index={idx} key={idx}>
                  {(prov, snap) => (
                    <motion.img
                      ref={prov.innerRef}
                      {...prov.draggableProps}
                      {...prov.dragHandleProps}
                      src={`data:image/svg+xml;base64,${btoa(c.rank + (c.suit || ''))}`}
                      width={40}
                      height={60}
                      animate={{
                        rotate: snap.isDragging ? 5 : 0,
                        scale: snap.isDragging ? 1.1 : 1,
                      }}
                      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                      style={{
                        boxShadow: snap.isDragging
                          ? '0 4px 8px rgba(0,0,0,0.3)'
                          : 'none',
                      }}
                    />
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
        <Droppable droppableId="discard">
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              style={{
                width: 40,
                height: 60,
                border: '1px solid black',
                background: snapshot.isDraggingOver ? '#f0f0f0' : 'transparent',
                transition: 'background 0.2s ease',
              }}
            >
              {state.discard_top && (
                <img
                  src={`data:image/svg+xml;base64,${btoa(
                    state.discard_top.rank + (state.discard_top.suit || '')
                  )}`}
                  width={40}
                  height={60}
                />
              )}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </div>
    </DragDropContext>
  );
}
