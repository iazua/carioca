from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel

from carioca.cards import Card
from carioca.hand import Hand
from carioca.round import Round
from carioca.melds import is_trio, is_scale


class GameState(BaseModel):
    round: Round
    current_player: int = 0
    melds: Dict[int, List[List[Card]]] = {}
    scores: List[int]
    total_rounds: int = 8
    finished: bool = False

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def new(cls, players: int, total_rounds: int = 8) -> "GameState":
        rnd = Round(1)
        rnd.start(players, cards_each=6)
        return cls(
            round=rnd,
            melds={i: [] for i in range(players)},
            scores=[0] * players,
            total_rounds=total_rounds,
            finished=False,
        )

    # Gameplay helpers --------------------------------------------------
    def draw(self, from_discard: bool = False) -> None:
        if from_discard:
            card = self.round.discard_pile.pop()
        else:
            card = self.round.draw_pile.draw()
        self.hand.take(card)

    def discard(self, index: int) -> Card:
        card = self.hand.discard(index)
        self.round.discard_pile.append(card)
        return card

    def next_player(self) -> None:
        self.current_player = (self.current_player + 1) % len(self.round.hands)

    @property
    def hand(self) -> Hand:
        return self.round.hands[self.current_player]

    def meld(self, indices: List[int]) -> bool:
        cards = [self.hand[i] for i in sorted(indices, reverse=True)]
        if is_trio(cards) or is_scale(cards):
            for i in sorted(indices, reverse=True):
                self.hand.pop(i)
            self.melds[self.current_player].append(cards)
            return True
        return False

    def can_close(self) -> bool:
        return not self.hand

    def close_round(self) -> None:
        # Very naive scoring: remaining card values
        for i, hand in enumerate(self.round.hands):
            self.scores[i] += sum(c.value for c in hand)
        next_num = self.round.number + 1
        if next_num <= self.total_rounds:
            self.round = Round(next_num)
            self.round.start(len(self.scores), cards_each=5 + next_num)
        else:
            self.round = Round(next_num)
            self.finished = True
        self.current_player = 0
        self.melds = {i: [] for i in range(len(self.scores))}
