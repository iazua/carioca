import React from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { motion } from 'framer-motion';
import { Card, GameState, MovePayload, Zone } from './types';
import { useDrag } from './hooks/useDrag';
import './GameBoard.css';

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
    const target = result.destination.droppableId as Zone;

    if (target === 'discard') {
      onMove({ type: 'discard', data: { card_id: cardId } });
      return;
    }
    if (target === 'table_meld') {
      onMove({ type: 'lay', data: { card_ids: [cardId] } });
      return;
    }
    if (target !== result.source.droppableId) {
      onMove({
        type: 'move',
        data: {
          card_ids: [cardId],
          source_zone: result.source.droppableId,
          target_zone: target,
        },
      });
    }
  }

  function draw(from: Zone) {
    onMove({ type: 'draw', data: { from } });
  }

  return (
    <div className="board">
      <div className="scoreboard">
        {state.players.map((p, i) => (
          <div
            key={p.id}
            className={`score ${i === state.current_turn ? 'currentPlayer' : ''}`}
          >
            {p.name ?? `Player ${i + 1}`}
          </div>
        ))}
      </div>

      <div className="zoneRow">
        <div
          className="pile"
          role="button"
          aria-label="stock"
          onClick={() => draw('stock')}
        >
          {state.stock_count}
        </div>

        <Droppable droppableId="discard">
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className="pile"
              aria-label="discard"
              onClick={() => draw('discard')}
              style={{
                background: snapshot.isDraggingOver ? '#f0f0f0' : undefined,
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

        <Droppable droppableId="table_meld" direction="horizontal">
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className="table"
              aria-label="table"
              style={{
                background: snapshot.isDraggingOver ? '#f9f9f9' : undefined,
              }}
            >
              {state.table_melds.map((meld, mi) => (
                <div key={mi} className="meld">
                  {meld.cards.map((c, ci) => (
                    <img
                      key={ci}
                      src={`data:image/svg+xml;base64,${btoa(c.rank + (c.suit || ''))}`}
                      width={40}
                      height={60}
                    />
                  ))}
                </div>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </div>

      <DragDropContext onDragEnd={handleDragEnd} onDragStart={(e) => onDragStart(e.source)}>
        <Droppable droppableId="player_hand" direction="horizontal">
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className="playerHand"
              style={{
                background: snapshot.isDraggingOver ? '#f0f0f0' : undefined,
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
                      width={60}
                      height={90}
                      animate={{
                        rotate: snap.isDragging ? 5 : 0,
                        scale: snap.isDragging ? 1.1 : 1,
                      }}
                      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                      className="card"
                    />
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
}
