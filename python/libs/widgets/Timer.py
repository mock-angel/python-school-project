# Timer.py
import time
class Timer():# Dead. Still used by minesweeper, but never tested positive.
    def __init__(self):
        self.current_time = time.time()
        
        self.state = 0
        
        self.total = 0
        
    def start(self):
        if not (self.state == 1):
            
            self.previous_time = time.time()
            self.state = 1
        
    def pause(self):
        if self.state == 1:
            self.state = 2
            self.current_time = time.time()
            self.total += self.current_time - self.previous_time
            
    def resume(self):
        if (self.state == 2):
            
            self.previous_time = time.time()
            self.state = 1
            
    def end(self):
        
        self.state = 0
        return self.total
        
        
    def reset(self):
        self.total = 0
        
    def is_paused(self):
        if (not self.state) or self.state == 2: return True
        else: return False
