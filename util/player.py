from typing import Optional
from util.card import Card, CardList, CardSuit

class Player:
    def __init__(self):
        self.cardInHand: CardList = CardList()
        self.cardFront: CardList = CardList()
    