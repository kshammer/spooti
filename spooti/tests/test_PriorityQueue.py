from spooti import PriorityQueue
import unittest

class testPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.pq = PriorityQueue.PriorityQueue()
        cool = [1,2,3,4]
        self.pq.setBase(cool)

    def tearDown(self):
        self.pq.clear()

    def test_isEmpty_true(self):
        self.assertTrue(self.pq.isEmpty())

    def test_isEmpty_false(self):
        self.pq.insert([1], 'ab', 1)
        self.assertFalse(self.pq.isEmpty())
        
    def test_single_pop(self):
        self.pq.insert([1], 'ab', 1)
        out = self.pq.pop()
        self.assertEqual(out, ([1], 'ab', 3, 1))
    
    def test_two_pop(self):
        self.pq.insert([1], 'ab', 1)
        self.pq.insert([1,2], 'cool', 1) # should what is popped out because it is closer 
        out = self.pq.pop()
        self.assertEqual(out, ([1,2], 'cool', 2, 1))

    def test_multi_pop(self):
        self.pq.insert([1], 'ab', 1)
        self.pq.insert([1,2], 'cool', 1)
        self.pq.insert([4,5,6], 'notcool', 1)
        self.pq.insert([1,2,3], 'int', 1)
        out1 = self.pq.pop()
        self.assertEqual(out1, ([1,2,3], 'int', 1, 1))
        out2 = self.pq.pop()
        self.assertEqual(out2, ([1,2], 'cool', 2, 1))
        