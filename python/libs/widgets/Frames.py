# Frames.py
'''
    Version: v1.0
    Authors: Anantha Krishna R.
'''

"""Frames - Use to calculate the framerate of the engines.
Usage: create an instance of the object and call init method of it.
To calculate the fps of a loop, just add a call to Framesobj.one_frame_execute()
"""
import time
import os

class Frames():
    def __init__(self):
        pass
    def init(self, message):
        self.message = message
        self.prev_time = time.time()
        self.current_time = time.time()
        
        self.total_time = 0
        self.frames = 0
        self.text = ""
    def one_frame_execute(self):
        
        self.current_time = time.time()
        
        self.time_difference = self.current_time - self.prev_time
        self.total_time += self.time_difference
        self.frames += 1
        
        if self.total_time >=1:
            self.total_time = 0
            print self.message, self.frames, "fps"
#            print os.system("ps aux | grep python | awk '{sum=sum+$6}; END {print sum/1024 \" MB\"}'")
            self.fps = self.frames
            self.frames = 0
        
        self.prev_time = self.current_time
