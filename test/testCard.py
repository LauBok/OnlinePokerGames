import sys
sys.path.append('.')
sys.path.append('./util')
import unittest
from util.card import Card, CardSuit

class testCard(unittest.TestCase):
    '''Test Card class'''
    
    def test_init(self):
        self.assertIsNone(Card().ID)
        self.assertEqual(Card(13).ID, 13)
        with self.assertRaises(TypeError):
            Card(2.4)
            Card('A10')
        with self.assertRaises(ValueError):
            Card(54)
            Card(-1)
    
    def test_suit(self):
        self.assertIsNone(Card().suit)
        self.assertEqual(Card(0).suit, CardSuit.Diamond)
        self.assertEqual(Card(12).suit, CardSuit.Diamond)
        self.assertEqual(Card(13).suit, CardSuit.Club)
        self.assertEqual(Card(25).suit, CardSuit.Club)
        self.assertEqual(Card(26).suit, CardSuit.Heart)
        self.assertEqual(Card(38).suit, CardSuit.Heart)
        self.assertEqual(Card(39).suit, CardSuit.Spade)
        self.assertEqual(Card(51).suit, CardSuit.Spade)
        self.assertEqual(Card(52).suit, CardSuit.Joker)
        self.assertEqual(Card(53).suit, CardSuit.Joker)

    def test_rank(self):
        self.assertIsNone(Card().rank)
        self.assertEqual(Card(0).rank, 0)
        self.assertEqual(Card(30).rank, 4)
        self.assertEqual(Card(52).rank, 0)
        self.assertEqual(Card(53).rank, 1)

if __name__ == "__main__":
    unittest.main()