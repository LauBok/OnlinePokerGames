import sys
sys.path.append('.')
sys.path.append('./util')
import unittest
from util.card import Card, CardSuit, CardList

class testCardList(unittest.TestCase):
    '''Test CardList class'''
    
    def test_init(self):
        self.assertListEqual(CardList().cardlist, [])
        self.assertListEqual(
            CardList([Card(13), Card(1), Card(2), Card(53)]).cardlist,
            CardList([Card(53), Card(13), Card(2), Card(1)]).cardlist
        )
        self.assertListEqual(
            CardList([Card(13), Card(13), Card(18), Card(8)]).cardlist,
            CardList([Card(18), Card(13), Card(13), Card(8)]).cardlist
        )
    
    def test_size(self):
        self.assertEqual(CardList().size, 0)
        self.assertEqual(CardList([Card(13), Card(13), Card(18), Card(8)]).size, 4)

    def test_len(self):
        self.assertEqual(len(CardList()), 0)
        self.assertEqual(len(CardList([Card(13), Card(13), Card(18), Card(8)])), 4)
    
    def test_isEmpty(self):
        self.assertEqual(CardList([]).isEmpty(), True)
        self.assertEqual(CardList([Card(3)]).isEmpty(), False)

    def test_insert(self):
        cl = CardList([Card(1), Card(15), Card(10)])
        cl.insert(Card(12))
        self.assertListEqual(cl.cardlist, [Card(15), Card(12), Card(10), Card(1)])
        cl.insert(CardList([Card(10), Card(10), Card(8)]))
        self.assertListEqual(
            cl.cardlist, 
            [Card(15), Card(12), Card(10), Card(10), Card(10), Card(8), Card(1)]
        )
    
    def test_insert_iadd(self):
        cl = CardList([Card(1), Card(15), Card(10)])
        cl += Card(12)
        self.assertListEqual(cl.cardlist, [Card(15), Card(12), Card(10), Card(1)])
        cl += CardList([Card(10), Card(10), Card(8)])
        self.assertListEqual(
            cl.cardlist, 
            [Card(15), Card(12), Card(10), Card(10), Card(10), Card(8), Card(1)]
        )
    
    def test_insert_add(self):
        cl = CardList([Card(1), Card(15), Card(10)])
        cl2 = cl + Card(12)
        self.assertListEqual(cl2.cardlist, [Card(15), Card(12), Card(10), Card(1)])
        cl3 = cl2 + CardList([Card(10), Card(10), Card(8)])
        self.assertListEqual(
            cl3.cardlist, 
            [Card(15), Card(12), Card(10), Card(10), Card(10), Card(8), Card(1)]
        )
        self.assertListEqual(cl.cardlist, [Card(15), Card(10), Card(1)])
    
    def test_remove_sub(self):
        cl = CardList([Card(1), Card(5), Card(10), Card(15)])
        cl2 = cl - Card(10)
        self.assertListEqual(cl2.cardlist, [Card(15), Card(5), Card(1)])
        with self.assertRaises(ValueError):
            cl2 - CardList([Card(1), Card(1)])
        cl4 = cl2 - CardList([Card(1), Card(5)])
        self.assertListEqual(cl4.cardlist, [Card(15)])
        self.assertListEqual(cl.cardlist, [Card(15), Card(10), Card(5), Card(1)])

    def test_count(self):
        cl = CardList([Card(1), Card(15), Card(10), Card(15), Card(30)])
        self.assertEqual(cl.count(Card(1)), 1)
        self.assertEqual(cl.count(1), 1)
        self.assertEqual(cl.count(Card(15)), 2)
        self.assertEqual(cl.count(15), 2)
        self.assertEqual(cl.count(Card(20)), 0)
        self.assertEqual(cl.count(20), 0)

    def test_count_getitem(self):
        cl = CardList([Card(1), Card(15), Card(10), Card(15), Card(30)])
        self.assertEqual(cl[Card(1)], 1)
        self.assertEqual(cl[1], 1)
        self.assertEqual(cl[Card(15)], 2)
        self.assertEqual(cl[15], 2)
        self.assertEqual(cl[Card(20)], 0)
        self.assertEqual(cl[20], 0)
    
    def test_contains(self):
        cl = CardList([Card(1), Card(15), Card(10), Card(15), Card(30)])
        self.assertEqual(Card(1) in cl, True)
        self.assertEqual(1 in cl, True)
        self.assertEqual(CardList([Card(1), Card(15)]) in cl, True)
        self.assertEqual([1, 15] in cl, True)
        self.assertEqual([15, 15] in cl, True)
        self.assertEqual([15, 15, 15] in cl, False)
    
    def test_filter_rshift(self):
        cl = CardList([Card(1), Card(15), Card(10), Card(15), Card(30), Card(48), Card(27)])
        self.assertListEqual(
            (cl >> CardSuit.filterSuit(CardSuit.Spade)).cardlist,
            [Card(48)]
        )
        self.assertListEqual(
            (cl >> CardSuit.filterSuit(CardSuit.Diamond | CardSuit.Heart)).cardlist,
            [Card(30), Card(27), Card(10), Card(1)]
        )
    
    def test_filter(self):
        cl = CardList([Card(1), Card(15), Card(10), Card(15), Card(30), Card(48), Card(27)])
        self.assertListEqual(
            (cl.filter(CardSuit.filterSuit(CardSuit.Spade))).cardlist,
            [Card(48)]
        )
        self.assertListEqual(
            (cl.filter(CardSuit.filterSuit(CardSuit.Diamond | CardSuit.Heart))).cardlist,
            [Card(30), Card(27), Card(10), Card(1)]
        )

if __name__ == "__main__":
    unittest.main()