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
        self.pq.insert([1], 'ab')
        self.assertFalse(self.pq.isEmpty())
        
    def test_single_pop(self):
        self.pq.insert([1], 'ab')
        out = self.pq.pop()
        self.assertEquals(out, ([1], 'ab', 3))
    
    def test_two_pop(self):
        self.pq.insert([1], 'ab')
        self.pq.insert([1,2], 'cool') # should what is popped out because it is closer 
        out = self.pq.pop()
        self.assertEquals(out, ([1,2], 'cool', 2))

    def test_multi_pop(self):
        self.pq.insert([1], 'ab')
        self.pq.insert([1,2], 'cool')
        self.pq.insert([4,5,6], 'notcool')
        self.pq.insert([1,2,3], 'int')
        out1 = self.pq.pop()
        self.assertEquals(out1, ([1,2,3], 'int', 1))
        out2 = self.pq.pop()
        self.assertEquals(out2, ([1,2], 'cool', 2))
        