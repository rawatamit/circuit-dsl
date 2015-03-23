class wire:
    def __init__(self):
        self.signal = 0
        self.actions = []
    
    def get_signal(self):
        return self.signal
    
    def set_signal(self, newval):
        if newval != self.signal:
            self.signal = newval
            # call each action procedure
            for action in self.actions:
                action()
    
    def add_action(self, action):
        self.actions.append(action)
        action() # call this action
