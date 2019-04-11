class PriorityQueue(object): 
    def __init__(self): 
        self.queue = []
        self.base = set()

    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 
  
    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == []
    
    def setBase(self, base):
        self.base = set(base)
  
    # inserts an element based on how different it is from the base set 
    def insert(self, data):
        data_set = set(data)
        intersection = self.base.intersection(data_set)
        diff = abs(len(self.base) - len(intersection)) # absolute value of the difference between the two sets 
        data_set_diff = (data_set, diff)
        if self.isEmpty():
            self.queue.append((data_set, diff)) # tuple of information and the difference from the base 

        # for the love of god someone help me flatten this function out 
        else:
            for elements in self.queue:
                if diff <= elements[1]:
                    self.queue.insert(self.queue.index(elements), data_set_diff)
                    break
        if data_set_diff not in set(self.queue):
            self.queue.append(data_set_diff)        
   
    def pop(self):
        return self.queue.pop(0)(0)