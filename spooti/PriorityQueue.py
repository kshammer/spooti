import sys
class PriorityQueue(object): 
    def __init__(self): 
        self.queue = []
        self.base = set()
        self.smallest = sys.maxsize

    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 
  
    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == 0

    def clear(self):
        self.queue = []
        self.base = set()
        self.smallest = sys.maxsize
    
    def setBase(self, base):
        self.base = set(base)
  
    # inserts an element based on how different it is from the base set 
    def insert(self, data, artist_id, depth):
        data_set = set(data)
        intersection = self.base.intersection(data_set)
        diff = abs(len(self.base) - len(intersection)) # absolute value of the difference between the two sets 
        if diff <= self.smallest:
            self.smallest = diff
        everything = (data, artist_id, diff, depth)
        self.queue.append(everything)
          
    def pop(self):
        next_smallest = list(filter(lambda x: x[2] <= self.smallest, self.queue))
        while(len(next_smallest) == 0 and not self.isEmpty()): # basically if the smallest ele is taken then it can't find the next smallest. This method is dumb and needs to be refactored 
            self.smallest += 1
            next_smallest = list(filter(lambda x: x[2] <= self.smallest, self.queue))
        output = next_smallest.pop(0)
        # have to remove because of 2 separate lists 
        self.queue.remove(output)
        return output