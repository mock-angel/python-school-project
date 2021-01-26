import pygame
from pygame.locals import *

import time
import random
from widgets import TextLine

STATIC = 1
DYNAMIC = 0

# Position match and audio match.

class Jack(pygame.sprite.Sprite):#NBack
    def __init__(self, obj):
        pygame.sprite.Sprite.__init__(self)
        
        self.back_ = obj
        
        # Alphabets are for audio and numbers represent visuals.
        
        # Load sequence first.
        self.alphabet_sequence = []
        self.number_sequence = []
        
        self.active_number = 0
        self.active_alphabet = None
        
        self.answer_count = 0
        self.answered_number = False
        self.answered_alphabet = False
        
        self.answered_count = 0
        self.failed_count = 0
        self.pattern_answered_count = 0
        self.audio_answered_count = 0
        
        # map(chr, range(ord('a'), ord('z')+1))
        self.allowed_alphabets = map(chr, range(97, 123)) 
        self.allowed_numbers = range(1, 10)
        
        self.max_sequence_count = 24
        self.back = 3
        self
        self.seq_len = 0 # Do not use this now.
        
        self.time_mode = STATIC
        self.feedback_on_error = True
        
        self.pick_list = (True, True, False, True, False, False)
        
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        
        self.tick_time = 0
        self.time_per_tick = 3
        
        self.clock = pygame.time.Clock()
        
        self.init_surfaces()
        self.center_rect()
        
    def init_surfaces(self):
        """Creates surfaces to be used position matching."""
        
        default_surf = pygame.image.load("data/board.png")
        blue_surf = pygame.image.load("data/blue.png")
        blue_rect = blue_surf.get_rect()
        
        _dict = {}
        
        _dict[0] = default_surf.copy()
        
        surf_1 = default_surf.copy()
        _dict[1] = surf_1
        
        surf_2 = default_surf.copy()
        _dict[2] = surf_2
        #surf_2.blit(blue_surf, (161, 1))
        
        surf_3 = default_surf.copy()
        _dict[3] = surf_3
        
        surf_4 = default_surf.copy()
        _dict[4] = surf_4
        
        surf_5 = default_surf.copy()
        _dict[5] = surf_5
        
        surf_6 = default_surf.copy()
        _dict[6] = surf_6
        
        surf_7 = default_surf.copy()
        _dict[7] = surf_7
        
        surf_8 = default_surf.copy()
        _dict[8] = surf_8
        
        surf_9 = default_surf.copy()
        _dict[9] = surf_9
        
        def get_center_pos(pos, size, division_diamension):
            width, height = size
            
            fx, fy = division_diamension
            
            x, y = pos
            
            offsetx, offsety = width/(fx) - width/(fx*2), height/(fy) - height/(fy*2)
            
            mulx, muly = width/fx, height/fx
            
            return offsetx + mulx * x, offsety + muly * y
        
        size = default_surf.get_size()
        grid_size = (3, 3)
        
        blue_rect.center = get_center_pos((0, 0), size, grid_size)
        surf_1.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((1, 0), size, grid_size)
        surf_2.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((2, 0), size, grid_size)
        surf_3.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((0, 1), size, grid_size)
        surf_4.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((1, 1), size, grid_size)
        surf_5.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((2, 1), size, grid_size)
        surf_6.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((0, 2), size, grid_size)
        surf_7.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((1, 2), size, grid_size)
        surf_8.blit(blue_surf, blue_rect)
        
        blue_rect.center = get_center_pos((2, 2), size, grid_size)
        surf_9.blit(blue_surf, blue_rect)
        
        self.number_surface_dict = _dict
        
        self.image = _dict[self.active_number]
    
    def center_rect(self):
        """---"""
        rect = pygame.display.get_surface().get_rect()
        
        centerx, centery = rect.width/2, rect.height/2
        rect = self.image.get_rect()
        rect.center = centerx, centery
        
        self.rect = rect
        
    def register(self, key):
        """register(key) - will be called on user press on a key on the keyboard.
        Can also be called when the action of 'a' or 'l' keys are replicated.
        
        Registers the answer if necessary after the user presses either the a or l keys.
        
        register() may mess up the memory while accessing the answered_alphabet
         and answered_number variables from different threads (event and update.)"""

        def on_a_pressed():
            """on_a_pressed() - replicates the action of an 'a' key press."""
            
            # If it was correct.
            if self.active_number == self.get_nback_number():
                self.answered_count += 1
                self.pattern_answered_count += 1
                print "'a' press registered : ", True
            
            # If user pressed on the wrong turn.
            else:
                
                self.failed_count += 1
                print "a press registered : ", False
                print self.number_sequence
                self.get_nback_number()
                
            self.answered_number = True
        
        def on_l_pressed():
            """on_l_pressed() - Replicates the action of an 'l' key press."""
            
            if self.active_alphabet == self.get_nback_alphabet():
                self.answered_count += 1
                self.audio_answered_count += 1
                print "'l' press registered : ", True
            
            else:
                self.failed_count += 1
                print "a press registered : ", False
                print self.alphabet_sequence
                print self.get_nback_alphabet()
            self.answered_alphabet = True
        
        # Call the required routines.
        
        if key == 'a' and not self.answered_number: on_a_pressed()
        if key == 'l' and not self.answered_alphabet: on_l_pressed()
    
    def get_nback_from_seq(self, seq):
        """get_nback_from_seq(seq) - returns the nback element for a
         provided sequence.
         
         """
        ret_value = None
        
        if len(seq) < self.back + 1: 
            ret_value = None
            
        else: 
            ret_value = seq[ -1 * (self.back + 1)]
        
        return ret_value
        
    def get_nback_alphabet(self):
        """get_nback_alphabet() - returns the nback alphabet."""
        
        return self.get_nback_from_seq(self.alphabet_sequence)
    
    def get_nback_number(self):
        """get_nback_number() - returns the nback alphabet."""
        
        return self.get_nback_from_seq(self.number_sequence)
    
    def new_tick(self):
        """new_tick() - Executes the next tick where the new elements are supposed to be added."""
        
        print "Ticked"
        
        # Check for the state of the previous tick.
        if len(self.number_sequence) > self.back and self.get_nback_number() == self.number_sequence[-1]:
            self.answer_count += 1
        if len(self.alphabet_sequence) > self.back and  self.get_nback_alphabet() == self.alphabet_sequence[-1]:
            self.answer_count += 1
        
        if self.answer_count >=self.max_sequence_count:
            self.exit()
        
        # Number
        if random.choice(self.pick_list) and len(self.number_sequence) > self.back:
            number = self.get_nback_from_seq(self.number_sequence + [0])
        else:
            number = random.choice(self.allowed_numbers)
        
        # Alphabet.
        if random.choice(self.pick_list) and len(self.alphabet_sequence) > self.back:
            alphabet = self.get_nback_from_seq(self.alphabet_sequence + ['0'])
        else:
            alphabet = random.choice(self.allowed_alphabets)
        
        self.active_number = number
        self.number_sequence.append(number)
        
        self.active_alphabet = alphabet
        self.alphabet_sequence.append(alphabet)
        
        self.answered_number = False
        self.answered_alphabet = False
        
        self.image = self.number_surface_dict[number]
        
        pygame.mixer.music.load("sound/" + alphabet + " (1).mp3")
        pygame.mixer.music.play()
    
    def exit(self):
        self.back_.end_screen(self)
        
    def update(self):
    
        # Choose random number and apply.
        self.tick_time += self.clock.tick()
        
        if self.tick_time > self.time_per_tick * 1000:
            self.tick_time = 0
            self.new_tick()
            
        else: pass
        
    def draw(self, surface):
        # Draw board.
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
