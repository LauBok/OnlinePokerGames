import sys
sys.path.append('.')
from util.game import Game
from util.func import Case
from util.card import Card, CardList, CardSuit
from util.player import Player
from typing import List, Optional, Tuple
import random

class LevelUp(Game):
    ### Constants
    PLAYERNUM: int = 4
    CARDPOOL: List[Card] = [Card(i) for i in range(54)] * 2
    BASESCORE: int = 80
    LEVELSCORE: int = 40

    def __init__(self):
        self.players: List[Optional[Player]] = [None] * LevelUp.PLAYERNUM
        self.discard_buffer: Optional[CardList] = None
        self.curPlayerIndex: Optional[int] = None
        self.rankLevel: Tuple[int, int] = (1, 1)
        self.dealerIndex: Optional[int] = None
        self.rankMain: int = 1
        # E.g. (Spade, 0, 1) means the main suit is spade (suited with a single spade by 0-th player)
        self.suitMain: Optional[Tuple(CardSuit, int, int)] = None
        self.score: int = 0
        self.state: str = 'END'
        for i in range(len(self.players)):
            self.players[i] = Player()
    
    
    def inform(self, information):
        case = Case(self.state)
        if case('END'):
            case = Case(information)
            if case('START'):
                self.state = 'DISPATCH'
                return (True, self._dispatch(), 
                    {
                        'suit': self.suitMain, 
                        'rank': self.rankMain,
                        'level': self.rankLevel
                    }
                )
        if case('DISPATCH'):
            case = Case(information)
            if case('FINISH'):
                self.state = 'DISCARD'
                if self.dealerIndex is None:
                    self.dealerIndex = self.suitMain[1]
                self.curPlayerIndex = self.dealerIndex
                self.players[self.curPlayerIndex].cardInHand += self.discard_buffer
                self.discard_buffer = CardList()
                for player in self.players:
                    player.cardFront = CardList()
                return (True, None, None)
        return (False, None, None)
    
    def _dispatch(self) -> List[int]:
        newCardPool: List[Card] = random.sample(LevelUp.CARDPOOL, len(LevelUp.CARDPOOL))
        dispatch = [newCardPool[0:25], newCardPool[25:50], newCardPool[50:75], newCardPool[75:100], newCardPool[100:]]
        for id, player in enumerate(self.players):
            player.cardInHand = CardList(dispatch[id])
        self.discard_buffer = CardList(dispatch[-1])
        return [[card.ID for card in cards] for cards in dispatch]
    
    def isSuitable(self, cards: List[int], playerID: int, suit: Optional[CardSuit] = None):
        #suit: 0 NT, 1 Spade, 2 Heart, 3 Club, 4 Diamond
        if suit is None:
            return [self.isSuitable(cards, playerID, s) for s in [
                CardSuit.Joker, CardSuit.Spade, CardSuit.Heart, CardSuit.Club, CardSuit.Diamond
            ]]
        cardnum = -1
        case = Case(suit)
        if case(CardSuit.Spade):  cardnum = 39 + self.rankMain
        elif case(CardSuit.Heart):  cardnum = 26 + self.rankMain
        elif case(CardSuit.Club):   cardnum = 13 + self.rankMain
        elif case(CardSuit.Diamond): cardnum = self.rankMain
        if self.suitMain is None:
            if suit == CardSuit.Joker:   
                return cards.count(52) == 2 or cards.count(53) == 2
            else:
                return cardnum in cards
        elif self.suitMain[1] == playerID:
            if self.suitMain[2] == 2:       return False
            if suit != self.suitMain[0]:    return False
            return cards.count(cardnum) == 2
        else:
            if suit == CardSuit.Joker:
                if self.suitMain[0] == CardSuit.Joker:
                    return cards.count(53) == 2
                else:
                    return cards.count(53) == 2 or cards.count(52) == 2
            if self.suitMain[2] == 2:   return False
            return cards.count(cardnum) == 2
    
    def suitRequest(self, playerID: int, suit: CardSuit):
        cards = self.players[playerID].cardInHand.tolist()
        if not self.isSuitable(cards, playerID, suit):
            return False
        for player in self.players:
            player.cardFront = CardList()
        cardnum = -1
        case = Case(suit)
        if case(CardSuit.Spade):  cardnum = 39 + self.rankMain
        elif case(CardSuit.Heart):  cardnum = 26 + self.rankMain
        elif case(CardSuit.Club):   cardnum = 13 + self.rankMain
        elif case(CardSuit.Diamond): cardnum = self.rankMain
        if suit == CardSuit.Joker:
            if cards.count(52) == 2:
                self.suitMain = (CardSuit.Joker, playerID, 2)
                self.players[playerID].cardFront += CardList([Card(52), Card(52)])
            else:
                self.suitMain = (CardSuit.Joker, playerID, 2)
                self.players[playerID].cardFront += CardList([Card(53), Card(53)])
        else:
            if self.suitMain is None:
                self.suitMain = (suit, playerID, 1)
                self.players[playerID].cardFront += Card(cardnum)
            else:
                self.suitMain = (suit, playerID, 2)
                self.players[playerID].cardFront += CardList([Card(cardnum), Card(cardnum)])
        front = [player.cardFront.tolist() for player in self.players]
        return [front, self.suitMain]
            