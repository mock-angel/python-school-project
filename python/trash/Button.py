
import sys
import ctypes
from sdl2 import *

import Golem
import property


class ButtonThemeFactory():
    def __init__(self):
        pass
    
    @staticmethod
    def genTheme(default = None, hover = None, held = None, disabled = None):
        hover = default if not hover else hover
        held = hover if not held else held
        
        dict_ = {   # refilter this.
            "sprite" : default,
            "clicked" : hover,
            "rclicked" : hover,
            
            "enter" : hover,
            "sprite_over" : hover,
            "leave" : default,
            
            "sprite_pressed" : held,
            "released" : hover,
            
            "sprite_disabled" : default,
        }
        
        return dict_
class ButtonBehaviour(property.SpriteBehaviour):
    SPRITE_DEFAULT = 0
    SPRITE_DISABLED = 1
    SPRITE_OVER = 2
    SPRITE_PRESSED = 3
    
    def __init__(self):
        property.SpriteBehaviour.__init__(self)
        
        self.AddSurface("sprite", None)
        self.AddSurface("sprite_over", None)
        self.AddSurface("sprite_pressed", None)
        self.AddSurface("sprite_disabled", None)
        
        self.AddTexture("sprite", None)
        self.AddTexture("sprite_over", None)
        self.AddTexture("sprite_pressed", None)
        self.AddTexture("sprite_disabled", None)
        
        self.renderState = ButtonBehaviour.SPRITE_DEFAULT;
        
        self.m_dirty = True
    
    def __del__(self):
        pass
    
    def updateTextures(self):
        Golem.property.SpriteBehaviour.updateTextures(self)
        print("updateTextures")
        self.GetSurface("sprite_over")
        if (self.reqSurface != None):
            createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.reqSurface)
            if (createdTexture != None): self.SetTexture("sprite_over", createdTexture )
        
        self.GetSurface("sprite_pressed")
        if (self.reqSurface != None):
            createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.reqSurface)
            if (createdTexture != None): self.SetTexture("sprite_pressed", createdTexture )
        
        self.reqSurface = None
        
        renderState = self.renderState
        
        if renderState == ButtonBehaviour.SPRITE_OVER:
            self.GetTexture("sprite_over")
            if (self.reqTexture != None): self.m_spriteTexture = self.reqTexture;
            w = ctypes.pointer(ctypes.c_int())
            h = ctypes.pointer(ctypes.c_int())
            SDL_QueryTexture(self.m_spriteTexture, None, None, w, h);
            self.m_rect.w, self.m_rect.h = w.contents, h.contents
            return
            
        if renderState == ButtonBehaviour.SPRITE_PRESSED:
            self.GetTexture("sprite_pressed")
            if (self.reqTexture != None): self.m_spriteTexture = self.reqTexture;
            SDL_QueryTexture(self.m_spriteTexture, None, None, ctypes.byref(self.m_rect.w), ctypes.byref(self.m_rect.h));
            return
    
    def onClicked(self):
        print("onClicked")
        if (self.m_disabled): return
        self.m_callbacks["onClicked"](self.m_params["onClicked"])
        
    def onReleased(self):
        print("onReleased")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_OVER;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onReleased"](self.m_params["onReleased"])
        
    def onPressed(self):
        print("onPressed")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_PRESSED;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onPressed"](self.m_params["onPressed"])
        
    def onRightClicked(self):
        print("onRightClicked")
        if (self.m_disabled): return
        self.m_callbacks["onRightClicked"](self.m_params["onRightClicked"])
        
    def onHover(self):
        print("onHover")
        if (self.m_disabled): return
        self.m_callbacks["onHover"](self.m_params["onHover"])
        
    def onEnter(self):
        print("onEnter")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_OVER;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onEnter"](self.m_params["onEnter"])
        
    def onLeave(self):
        print("onLeave")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_DEFAULT;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onLeave"](self.m_params["onLeave"])
        
class BasicButton(ButtonBehaviour, property.Sprite):
    def __init__(self, t_window):
        
        property.Sprite.__init__(self, t_window)
        ButtonBehaviour.__init__(self)
        self.m_renderTarget = t_window.getRenderer() if t_window else None
        
    def set_pos(self, x, y):
        self.rect
        return self
    
    def setTheme(self, t_theme): # TODO: Make this function invisible?
        self.m_theme = t_theme
        self.enscribeTheme(("sprite", "sprite_over", "sprite_pressed", "sprite_disabled"), t_theme)
        return self
    
class Button(BasicButton):
    def __init__(self, t_window):
        BasicButton.__init__(self, t_window)
        
    def setText(self, t_text):
        self.m_text = t_text
        return self

