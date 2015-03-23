import heapq

class agenda:
    def __init__(self):
        self.curtime = 0
        self.counter = 0
        self.actions = []
    
    def get_curtime(self):
        return self.curtime
    
    def is_empty(self):
        return len(self.actions) == 0
    
    def add_action(self, action, time):
        heapq.heappush(self.actions, (time, self.counter, action))
        self.counter += 1
    
    def first_action(self):
        return self.actions[0]
    
    def remove_first_action(self):
        first_action = self.first_action()
        self.curtime = first_action[0]
        heapq.heappop(self.actions)
        return first_action[2]
