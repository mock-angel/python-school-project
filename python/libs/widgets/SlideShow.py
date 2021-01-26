# SlideShow.py
"""
        7-9-2018
"""
import random
import time
import pygame

class SlideShow(): # Used mainly by UI to perform slideshow animation at background.
    def __init__(self):
        
        self.size = pygame.display.get_surface().get_size()
        self.rect = pygame.Rect((0, 0, self.size[0], self.size[1]))
        
        self.time_per_frame = 2
        
        self.raw_slide_set = dict()
        self.slide_set = dict()
        
        self.index = 0
        
        self.previous_time = time.time()
        self.current_time = self.previous_time
        
        self.time_per_frame = 10
        self.transition_time = 2
        
        self.current_frame_index = 0
        self.previous_frame_index = 0
        
        self.random_show = True
        
        self.alpha_surface = pygame.Surface(self.size)
        self.alpha_surface.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MIN)
        self.alpha = 0
        
        self.current_surface = None
        
    def set_time_per_slide(self, time_):
        """set_time_per_slide() -Set max secs the slide is viewed before its changed."""
        
        self.time_per_frame = time_
    
    def set_transition_time(self, time_):
        """set_transition_time() - set the time needed to switch between slides,
        ie keep 2 slides at the same time."""
        
        self.transition_time = time_
        
    def set_size_of_slide(self, size):
        self.size = size
    
    def add_slide(self, frame):
        """add_slide() - Method to add new slide to the slideshow."""
        
        img_scale = pygame.transform.scale
        
        self.raw_slide_set[self.index] = frame.convert_alpha()
        self.slide_set[self.index] = img_scale(frame, self.size).convert_alpha()
        self.slide_set[self.index].set_alpha(0)
        
        self.index += 1
        self.update()
        
    def get_random_slide(self):
        
        r_list = range(0, self.index)
        if self.index: r_list.remove(self.current_frame_index) # Choose unique.
        return random.choice(r_list)
        
    def get_next(self):
        curr_i = self.current_frame_index
        return curr_i +1 if (curr_i + 1) <= self.index else 0 
    
    
    def update(self):
        current_time = self.current_time = time.time()
        time_diff = current_time - self.previous_time
        
        # If time exceeded time_per_frame, display random/next slide.
        if time_diff > self.time_per_frame:
            
            self.previous_time = current_time
            
            frame_index=self.get_random_slide() if self.random_show else self.get_next()
            self.alpha = 0
            
            self.previous_frame_index = self.current_frame_index
            self.current_frame_index = frame_index
            
        # If screen transition is required after slide change.
        if time_diff < self.transition_time:
            alpha = self.alpha = (time_diff/self.transition_time) * 255
            
            surf_curr = self.alpha_surface.copy()
            surf_prev = self.alpha_surface.copy()
            
            surf_curr.set_alpha(alpha)
            surf_prev.set_alpha(255 - alpha)
            
            prev_img = self.slide_set[self.previous_frame_index]
            surf_prev.blit(prev_img, (0, 0))
            
            curr_img = self.slide_set[self.current_frame_index]
            surf_curr.blit(curr_img, (0, 0))
            self.current_surface = surf_curr
            self.previous_surface = surf_prev
            
    def draw(self, surface):
    
        # Draw previous slide if its still in transition, else skip.
        if self.slide_set.has_key(self.previous_frame_index) and self.alpha < 255:
            self.slide_set[self.previous_frame_index].set_alpha(0)
            surface.blit(self.previous_surface, self.rect)
        
        # Always draw current image if the key exists.
        if self.slide_set.has_key(self.current_frame_index):
            self.slide_set[self.current_frame_index].set_alpha(0)
            surface.blit(self.current_surface, self.rect)
