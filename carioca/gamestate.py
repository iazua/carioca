from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
from collections import deque

from .cards import Card, Suit
from .deck import Deck
from .hand import Hand
from .round import Round
from .melds import is_trio, is_scale


# ---------------------------------------------------------------------------
# Helpers for serialisation
# ---------------------------------------------------------------------------
def _card_to_dict(card: Card) -> dict:
    return {"rank": card.rank, "suit": card.suit.name if card.suit else None}


def _card_from_dict(data: dict) -> Card:
    suit = Suit[data["suit"]] if data["suit"] is not None else None
    return Card(data["rank"], suit)


def _deck_to_list(deck: Deck) -> List[dict]:
    return [_card_to_dict(c) for c in deck._cards]


def _deck_from_list(cards: List[dict]) -> Deck:
    deck = Deck()
    deck._cards = deque(_card_from_dict(c) for c in cards)
    return deck


def _hand_to_list(hand: Hand) -> List[dict]:
    return [_card_to_dict(c) for c in hand]


def _hand_from_list(cards: List[dict]) -> Hand:
    hand = Hand()
    hand.extend(_card_from_dict(c) for c in cards)
    hand.sort()
    return hand


def _round_to_dict(rnd: Round) -> dict:
    return {
        "number": rnd.number,
        "draw_pile": _deck_to_list(rnd.draw_pile),
        "discard_pile": [_card_to_dict(c) for c in rnd.discard_pile],
        "hands": [_hand_to_list(h) for h in rnd.hands],
    }


def _round_from_dict(data: dict) -> Round:
    rnd = Round(data["number"])
    rnd.draw_pile = _deck_from_list(data["draw_pile"])
    rnd.discard_pile = [_card_from_dict(c) for c in data["discard_pile"]]
    rnd.hands = [_hand_from_list(h) for h in data["hands"]]
    return rnd


@dataclass
class GameState:
    round: Round
    current_player: int = 0
    melds: Dict[int, List[List[Card]]] = field(default_factory=dict)
    scores: List[int] = field(default_factory=list)
    total_rounds: int = 8

    @classmethod
    def new(cls, players: int, total_rounds: int = 8) -> "GameState":
        rnd = Round(1)
        rnd.start(players, cards_each=6)
        return cls(
            round=rnd,
            current_player=0,
            melds={i: [] for i in range(players)},
            scores=[0] * players,
            total_rounds=total_rounds,
        )

    # ------------------------------------------------------------------
    # Gameplay helpers
    # ------------------------------------------------------------------
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
        for i, hand in enumerate(self.round.hands):
            self.scores[i] += sum(c.value for c in hand)
        self.round = Round(self.round.number + 1)
        if self.round.number <= self.total_rounds:
            self.round.start(len(self.scores), cards_each=5 + self.round.number)
        self.current_player = 0
        self.melds = {i: [] for i in range(len(self.scores))}

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "round": _round_to_dict(self.round),
            "current_player": self.current_player,
            "melds": {
                str(p): [[_card_to_dict(c) for c in meld] for meld in ms]
                for p, ms in self.melds.items()
            },
            "scores": self.scores,
            "total_rounds": self.total_rounds,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        rnd = _round_from_dict(data["round"])
        melds = {
            int(p): [[_card_from_dict(c) for c in meld] for meld in ms]
            for p, ms in data.get("melds", {}).items()
        }
        return cls(
            round=rnd,
            current_player=data.get("current_player", 0),
            melds=melds,
            scores=data.get("scores", []),
            total_rounds=data.get("total_rounds", 8),
        )
