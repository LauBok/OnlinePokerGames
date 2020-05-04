from __future__ import annotations
from enum import unique, Enum, IntFlag
from dataclasses import dataclass
from typing import Optional, List, Callable, Union
from func import Case
from functools import singledispatch

@unique
class CardSuit(IntFlag):
    Spade = 1,
    Heart = 2,
    Club = 4,
    Diamond = 8,
    Joker = 16

    @staticmethod
    def filterSuit(filter: int) -> Callable[[Card], bool]:
        return lambda card: card.suit & filter != 0
    

@dataclass
class Card:
    '''
    The class for a playing card, identified by an integer ranged 0 to 53.

    ID: (default None) The identifier
        0 - 12: Diamond, Ace to King
        13 - 25: Club, Ace to King
        26 - 38: Heart, Ace to King
        39 - 51: Spade, Ace to King
        52: Black Joker
        53: Red Joker
    '''

    ID: Optional[int] = None

    def __post_init__(self):
        if self.ID is None:
            return
        if not isinstance(self.ID, int):
            raise TypeError('Card ID should be an integer.')
        if self.ID < 0 or self.ID > 53:
            raise ValueError('Card ID should be in range (0, 54).')

    @property
    def suit(self) -> Optional[CardSuit]:
        '''Return the suit type of the card'''
        if self.ID is None:
            return None
        case = Case(self.ID)
        if case(13):    return CardSuit.Diamond
        elif case(26):  return CardSuit.Club
        elif case(39):  return CardSuit.Heart
        elif case(52):  return CardSuit.Spade
        else:           return CardSuit.Joker

    @property
    def rank(self) -> Optional[int]:
        '''
        Return the rank of the card.
        Value:  0(Ace) - 12(King)
                0(Black Joker), 1(Red Joker)
        '''
        if self.ID is None:
            return None
        case = Case(self.ID)
        if case(52):    return self.ID % 13
        else:           return self.ID - 52

    def _suit_str(self) -> str:
        suit = self.suit
        if suit is None:                return 'None'
        if suit == CardSuit.Spade:      return u'\u2660'
        if suit == CardSuit.Heart:      return u'\u2665'
        if suit == CardSuit.Club:       return u'\u2663'
        if suit == CardSuit.Diamond:    return u'\u2666'
        if suit == CardSuit.Joker:      return 'Joker'
        raise ValueError('Undefined suit type.')

    def _rank_str(self) -> str:
        rank = self.rank
        if rank is None:    return 'None'
        if Case(rank)(1):   return 'A'
        if Case(rank)(10):  return str(rank + 1)
        if Case(rank)(11):  return 'J'
        if Case(rank)(12):  return 'Q'
        if Case(rank)(13):  return 'K'
        raise ValueError('Undefined rank value.')

    ### operator methods
    
    def __str__(self) -> str:
        if self.ID is None:
            return 'None'
        if self.ID == 52:   return 'Joker'
        if self.ID == 53:   return 'JOKER'
        return self._suit_str() + self._rank_str()
    
    def __repr__(self) -> str:
        return str(self)
    

class CardList:
    '''
    Class for a list of cards.
    '''

    hashfunc: Callable[[Card], int] = lambda card: -1 if card is None else card.ID

    def __init__(self, cardlist: Optional[List[Card]] = None):
        if cardlist is None:
            self.cardlist = []
        else:
            self.cardlist = cardlist
        self._sort()

    @property
    def size(self) -> int:
        '''Return the number of cards in the list'''
        return len(self.cardlist)

    def isEmpty(self) -> bool:
        '''check if the current list is empty'''
        return self.size == 0
    
    def insert(self, cards: Union[Card, CardList]) -> None:
        '''
        Insert a card or a list of card into current card list.
        The list will automatically keep sorted.
        The current object will be modified.
        '''
        if isinstance(cards, Card):
            self._insert_no_sort(cards)
        elif isinstance(cards, CardList):
            for card in cards.cardlist:
                self._insert_no_sort(card)
        else:
            raise TypeError("Argument 1 should be an instance of Card or CardList.")
        self._sort()
    
    def remove(self, cards: Union[Card, CardList]) -> None:
        if not cards in self:
            raise ValueError("CardList.remove(cards): cards not in card list")
        if isinstance(cards, Card):
            self.cardlist.remove(cards)
        else:
            for card in cards.cardlist:
                self.cardlist.remove(card)
    
    def count(self, card: Union[Card, int]) -> int:
        '''
        Return count of how many time a card appears in the list.
        The card can be a Card object or an integer showing the ID.
        '''
        if isinstance(card, Card):
            card_ID = card.ID
        else:
            card_ID = card
        return [c.ID == card_ID for c in self.cardlist].count(True)

    def filter(self, pred: Callable[[Card], bool]) -> CardList:
        '''
        Return a filtered sublist according to a predicate.
        '''
        return CardList([card for card in self.cardlist if pred(card)])
    
    ### operator methods

    def __len__(self) -> int:
        '''Return the number of cards in the list'''
        return self.size

    def __str__(self) -> str:
        return f'CardList of length {self.size}: ' + str(self.cardlist)
    
    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, card: Union[Card, int]) -> int:
        '''
        Return count of how many time a card appears in the list.
        '''
        return self.count(card)
    
    def __contains__(self, cards: Union[Card, int, CardList]) -> bool:
        '''
        Check if another card or cardlist is contained in the list.
        '''
        if isinstance(cards, Card) or isinstance(cards, int):
            return self[cards] > 0
        # check for each card
        if isinstance(cards, CardList):
            for card in cards.cardlist:
                if self[card] < cards[card]:
                    return False
        elif isinstance(cards, list):
            for card in cards:
                if self[card] < cards.count(card):
                    return False
        else:
            raise TypeError("Unknown type for argument 1.")
        return True

    def __add__(self, cards: Union[Card, CardList]) -> CardList:
        '''
        Insert a card or a list of card into current card list.
        The current object will NOT be modified.
        Instead, a new object will be created
        Operator: +
        '''
        copyCardList = self._copy()
        copyCardList.insert(cards)
        return copyCardList
    
    def __sub__(self, cards: Union[Card, CardList]) -> None:
        '''
        Insert a card or a list of card into current card list.
        The current object will be modified.
        Operator: +=
        '''
        copyCardList = self._copy()
        copyCardList.remove(cards)
        return copyCardList

    def __iadd__(self, cards: Union[Card, CardList]) -> None:
        '''
        Insert a card or a list of card into current card list.
        The current object will be modified.
        Operator: +=
        '''
        self.insert(cards)
        return self

    def __isub__(self, cards: Union[Card, CardList]) -> None:
        '''
        Insert a card or a list of card into current card list.
        The current object will be modified.
        Operator: +=
        '''
        self.remove(cards)
        return self

    def __rshift__(self, pred: Callable[[Card], bool]) -> CardList:
        return self.filter(pred)

    ### private methods
    
    def _sort(self) -> CardList:
        self.cardlist = sorted(self.cardlist, key = CardList.hashfunc, reverse = True)
        return self

    def _copy(self) -> CardList:
        return CardList(self.cardlist.copy())
    
    def _insert_no_sort(self, card: Card) -> None:
        self.cardlist.append(card)

if __name__ == "__main__":
    a = CardList([Card(52),Card(53),Card(24),Card(10), Card(10)])
    b = a + Card(20)
    b += CardList([Card(13),Card(39)])
    b -= Card(20)
    print(b)
    print(b - CardList([Card(10), Card(10)]))
    print(b >> CardSuit.filterSuit(CardSuit.Spade | CardSuit.Joker))