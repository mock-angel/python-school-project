# Panel.py
"""Note: Its not necessary to understand this script since its the widgets backend."""

import pygame
from pygame.locals import *

from Mouse import Mouse

class Panel(pygame.sprite.LayeredUpdates):
    """One time panel. Onlly one object collided with mouse can recieve events."""
    __li = []
    __p = None
    @staticmethod
    def get_first():
        return Panel.__li[0]
    
    @staticmethod
    def get_primary():
        return Panel.__p
    def __init__(self):
        #super(Panel, self).__init__()
        pygame.sprite.LayeredUpdates.__init__(self)
        self.__li.append(self)
        self.Mouse = Mouse()
        self.disabled = False
        
    def set_primary(self):
        Panel.__p = self
        
    def provide_event(self, spr, event):
        
        # Mouse section.
        if event.type == pygame.MOUSEBUTTONDOWN:
            spr.on_event("start_clicked", event.button, event)
            spr.on_event("pressed", event.button, event)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            spr.on_event("released", pyevent = event)

        elif event.type == pygame.MOUSEMOTION:

            spr.on_event("hover", pyevent=event)
            pass
            
    def on_key_event(self, event):
        
        sprites = self.sprites()
        for spr in sprites:
            spr.on_key_event(event, pygame.key.name(event.key))
    def update(self, events = None):
        # Seperate some to different methods.
        
        if self.disabled == True:
            return
        
        sprites = self.sprites()
        
        processed_sprites = set()
        
        for event in events:
            
            # check for keyboard event first:
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.on_key_event(event)
                continue
                
            try:
                x, y = event.pos
                
            except:
                continue
                
             
            self.Mouse.rect = pygame.Rect(x, y, 1, 1)
            self.Mouse.update()
            sprites_at_point = self.get_sprites_at(event.pos)
            
            done = False
            layer = -1000
            
            while sprites_at_point:
                spr = sprites_at_point.pop()
                
                # MOdifier.
                if not spr.disabled: 
                    self.provide_event(spr, event)
                    break
                    
                else: pass
                
                processed_sprites.add(spr)
                
        unprocessed_sprites =  (set(sprites) - processed_sprites) 
        
        self.Mouse.update()
        
        # TODO: This code needs to be rewritten. Its a little crap and doesthe job, 
        # but find another way.
        
        # It does release the drag and helps call the on_release() on drag.
        # Wirthout this , the drag won't relase. A total script rewite may be a 
        # necessity.
        mouse_idle_hover_sprites = set(pygame.sprite.spritecollide(self.Mouse, self, False)) - processed_sprites
        unprocessed_sprites -= mouse_idle_hover_sprites
        
        unprocessed_sprites = list(unprocessed_sprites)
        
        #processed_sprites |= set(pygame.sprite.spritecollide(self.Mouse, self, False))

        for spr in unprocessed_sprites:
            
            spr.on_event("idle")
    def disable(self):
        self.disabled = True
        
    def enable(self):
        self.disabled = False


class PanelLayered(Panel): # Used by Pdtb app.

    def __init__(self):
        Panel.__init__(self)
        
    def make_focus_dict(self, sprites):
        
        dict_ = {
            0 : [],
            1 : [],
            2 : [],
            3 : [],
            4 : [],
        }
        for spr in sprites:
            dict_[spr.focus].append(spr)
        
        return dict_
        
    def update(self, events = None):
        sprites = self.sprites()
        
        processed_sprites = set()
        
        for event in events:
            try:
                x, y = event.pos
            except:
                continue
                
             
            self.Mouse.rect = pygame.Rect(x, y, 1, 1)
            
            sprites_at_point = self.get_sprites_at(event.pos)
            focus_dict = self.make_focus_dict(sprites_at_point)
            
            done = False
            layer = -1000
            
            for key in focus_dict:
                
                while sprites_at_point:
                    spr = sprites_at_point.pop()
                    spr_lyr = self.get_layer_of_sprite(spr)
                    
                    if spr_lyr<layer and done:
                        break
                    layer = spr_lyr
                    done = True
                    
                    self.provide_event(spr, event)
                    processed_sprites.add(spr)
#                    print spr, "lll"
                if done:
                    break
                
        unprocessed_sprites =  (set(sprites) - processed_sprites) 
        
        self.Mouse.update()
        # TODO: This code needs to be rewritten. Its a little crap and doesthe job, 
        # but find another way.
        
        # It does release the drag and helps call the on_release() on drag.
        # Wirthout this , the drag won't relase. A total script rewite may be a 
        # necesity.
        mouse_idle_hover_sprites = set(pygame.sprite.spritecollide(self.Mouse, self, False)) - processed_sprites
        unprocessed_sprites -= mouse_idle_hover_sprites
        
        unprocessed_sprites = list(unprocessed_sprites)
        
        #processed_sprites |= set(pygame.sprite.spritecollide(self.Mouse, self, False))

        for spr in unprocessed_sprites:
            
            spr.on_event("idle")
