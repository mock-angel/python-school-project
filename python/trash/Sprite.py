
import sys
import ctypes
from sdl2 import *

import Golem
import threading

NULL = 0

class SpriteBehaviour(object):
    SPRITE_DEFAULT = 0
    SPRITE_DISABLED = 1
    def __init__(self):
        self.m_sprTextures = {}
        self.m_sprSurfaces = {} # TODO:Change to surfaceMap?
        
        self.m_surfaceLock = threading.Lock()
        self.m_textureLock = threading.Lock() # FIXME: Not used
        
        self.reqTexture = None
        self.reqSurface = None
        self.selectedSurface = None
        
        self.m_renderTarget = None# FIXME: First import  all behaviours
        self.renderState = SpriteBehaviour.SPRITE_DEFAULT
        
        self.AddSurface("sprite", None)
        self.AddSurface("sprite_disabled", None)
        
        self.AddTexture("sprite", None)
        self.AddTexture("sprite_disabled", None)
        
        self.m_origin = {
            # Defines the owership of the contained object.
            "Surfaces":[],
            "Textures":[],
            "Renderer":[],
        }
        
        #self.SetSurface("sprite", Golem.loadSurface("golem.png"))
        
    def __del__(self):
        print("~deleted SpriteBehaviour")
        for surf in self.m_origin["Surfaces"]:
            SDL_DestroyTexture(surf)
            
        for texture in self.m_origin["Textures"]:
            SDL_DestroyTexture(texture)
        
        for renderer in self.m_origin["Renderer"]:
            SDL_DestroyRenderer(renderer)
            
    def AddSurface(self, string, t_surface):
        
        self.m_surfaceLock.acquire()
        if string in self.m_sprSurfaces:
            self.m_surfaceLock.release()
            return None
        
        self.m_sprSurfaces[string] = t_surface
        self.m_surfaceLock.release()
        
    def SetSurface(self, string, t_surface):
        self.m_surfaceLock.acquire()
        print ("SetSurface :", string)
        if string not in self.m_sprSurfaces:
            self.m_surfaceLock.release()
            return None
            
        self.m_sprSurfaces[string] = t_surface 
        self.m_surfaceLock.release()
    
    def GetSurface(self, string):
        self.m_surfaceLock.acquire()
        if string not in self.m_sprSurfaces:
            print ("Button::GetSurface: key non-existant.")
            self.m_surfaceLock.release()
            return None
            
        self.reqSurface = self.m_sprSurfaces[string]
        self.m_surfaceLock.release()
        return self.reqSurface # FIXME: Used reqSUrface instead of m_sprSurfaces[string]
        
    def SelectSurface(self, string):            # For user use only.
        self.m_surfaceLock.acquire()
        if string not in self.m_sprSurfaces:
            print("SelectSurface(): Key does not exist.")
            self.m_surfaceLock.release()
            return None
        self.selectedSurface = self.m_sprSurfaces[string]
        self.m_surfaceLock.release()
        
    def AddTexture(self, string, t_surface):    #
        if string in self.m_sprTextures:
            print("AddTexture(): Key allready exists.")
            return None
        
        self.m_sprTextures[string] = t_surface
        
    def SetTexture(self, string, t_surface):    #Thread Friendly method.
        if string not in self.m_sprTextures:
            print("AddTexture(): Key does not exist.")
            return None
            
        self.m_sprTextures[string] = t_surface
        
    def GetTexture(self, string ):
        #Render thread Only.
        if string not in self.m_sprTextures:
            print("GetTexture(): key non-existant.")
            return None;
        self.reqTexture = self.m_sprTextures[string]
        return self.m_sprTextures[string]

    def updateTextures(self):
        self.GetSurface("sprite")
        if (self.reqSurface != None):
            createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.reqSurface)
            if (createdTexture != None): self.SetTexture("sprite", createdTexture )
        
        self.GetSurface("sprite_disabled")
        if (self.reqSurface != None):
            createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.reqSurface)
            if (createdTexture != None): self.SetTexture("sprite_disabled", createdTexture )
        
        self.reqSurface = None
        
        renderState = self.renderState
        
        if renderState == SpriteBehaviour.SPRITE_DEFAULT:
            self.GetTexture("sprite")
            if (self.reqTexture != None): self.m_spriteTexture = self.reqTexture;
            
            w = ctypes.pointer(ctypes.c_int())
            h = ctypes.pointer(ctypes.c_int())
            SDL_QueryTexture(self.m_spriteTexture, None, None, w, h);
            
            self.m_rect.w = w.contents.value
            self.m_rect.h = h.contents.value
            
            return
            
        if renderState == SpriteBehaviour.SPRITE_DISABLED:
            self.GetTexture("sprite_disabled")
            if (self.reqTexture != None): self.m_spriteTexture = self.reqTexture;
            
            w = ctypes.pointer(ctypes.c_int())
            h = ctypes.pointer(ctypes.c_int())
            SDL_QueryTexture(self.m_spriteTexture, None, None, self.m_rect.w, self.m_rect.h);
            
            self.m_rect.w = w.contents.value
            self.m_rect.h = h.contents.value
            return
            
        self.reqTexture = None
    
    def enscribeTheme(self, keyList, t_theme):
        for key in keyList:
            if key in t_theme:
                self.SetSurface(key, t_theme[key])
    
class SpriteTextureOwnership(object):
    def __init__(self):
        self.m_OwningTextures
class Sprite(SpriteBehaviour, object):
    DEFAULTWINDOW = None
    RECENTWINDOW = None
    
    def __init__(self, t_window):
        SpriteBehaviour.__init__(self)
        
        Sprite.RECENTWINDOW = t_window
        
        self.m_mouseOver = False
        self.m_pressed = False
    
        self.m_visible = True
        self.m_disabled = False #Used to be m_spriteSettingDisabled
        
        self.m_depth = 0
        
        self.m_spriteTexture = None
        self.m_spriteSurface = None
        
        self.m_renderTarget = t_window.getRenderer() if t_window else None
        print ("Printing render stare : ", self.m_renderTarget)
#        if not self.m_renderTarget:
#            Golem.log_error("Sprite.__init__(self): created without any renderTarget.")
        
        self.m_rect = Golem.Rect((0, 0), (500, 500))#Golem.Rect()
        self.rect = self.m_rect
        
        self.m_disabled = False
        
        self.m_callbacks = {
            "onClicked": self.onDummy,
            "onReleased": self.onDummy,
            "onPressed": self.onDummy,
            "onRightClicked": self.onDummy,
            "onHover": self.onDummy,
            "onEnter": self.onDummy,
            "onLeave": self.onDummy,
        }
        
        params = list()
        self.m_params = {
            "onClicked": params,
            "onReleased": params,
            "onPressed": params,
            "onRightClicked": params,
            "onHover": params,
            "onEnter": params,
            "onLeave": params,
        }
        
        self.m_mouseOver = False
        self.m_visible = True
        self.m_disabled = False
        self.m_pressed = False
        
        self.buffer_flag = True;
    
    def __del__(self):
        
        SpriteBehaviour.__del__(self)
        print("~deleted Sprite")
        
    def setVisible(self, boolean):
        m_visible = bool(boolean)
        return self
        
    def disable(self):
        self.m_disabled = True
        return self
    
    def enable(self):
        self.m_disabled = False
    
    def isDisabled(self):
        return m_disabled
        
    def getRenderer(self):
        return self.m_renderTarget
        
    def setTexture(self, t_texture):
        self.m_spriteTexture = self.t_texture
        #self.m_rect.w, self.m_rect.h = t_texture.contents.w, t_texture.contents.h
        
    def setRenderer(self, t_pRenderer):
        self.m_renderTarget = t_pRenderer
    
    def setVisible(self, t_visible):
        self.m_visible = t_visible
    
    def disable(self):
        self.m_disabled = True
    
    def enable(self):
        self.m_disabled = False
    
    def isDisabled(self):
        return self.m_disabled
    
    # Setters
    @property
    def depth(self):
        return m_depth
    
    @depth.setter
    def depth(self, d):
        self.m_depth = d
        return self
        
    # Called by handleEvent thread.
    def handleEvent(self, e):
        pass
    
    # Called by update Thread when not Disabled.
    def update(self):
        pass
    
    # Used by user to Draw sprite onto a surface.
    def draw(self, t_surface):
        if (not self.m_visible): return
        if (SDL_BlitSurface(self.m_spriteSurface, None, self.t_surface, self.m_rect) < 0):
            print(SDL_GetError())
    
    # Called by render Thread when sprite is visible.
    def render(self):
        if (not self.m_visible): return
        
        if self.m_dirty:# FIXME: FIND this ones purpose
            self.m_dirty = False
#        if t_texture:
#            SDL_SetRenderTarget( self.m_cRenderer, t_texture )
#            SDL_RenderCopy(self.m_cRenderer, self.m_spriteTexture, NULL, ctypes.byref(self.m_rect))
#            SDL_SetRenderTarget( self.m_cRenderer, NULL )
        #if self.m_dirty:    # If the sprite needs to be redrawn?
        #    self.m_dirty = False;
        #    self.generateButtonSprite()
        
        if self.buffer_flag:# If some changes were done using SetSurfaces or AddSurfaces.
            self.buffer_flag = False
            self.updateTextures()
        
        if (SDL_RenderCopy(self.m_renderTarget, self.m_spriteTexture, None, self.m_rect)<0):
            print(SDL_GetError())
            
    def onDummy(self, *params):
        pass
    
    def onClicked(self):
        self.callbacks["onClicked"](*self.m_params["onClicked"])
        
    def onReleased(self):
        self.m_callbacks["onReleased"](*self.m_params["clicked"])
    
    def onPressed(self):
        self.m_callbacks["onPressed"](*self.m_params["onPressed"])
    
    def onRightClicked(self):
        self.m_callbacks["onRightClicked"](*self.m_params["onRightClicked"])
    
    def onHover(self):
        self.m_callbacks["onHover"](*self.m_params["onHover"])
    
    def onEnter(self):
        self.m_callbacks["onEnter"](*self.m_params["onEnter"])
        print("ENtered")
    def onLeave(self):
        self.m_callbacks["onLeave"](*self.m_params["onLeave"])
    
class SpriteGroup():
    def __init__(self):
        self.m_container = list()
        self.containerRenderLock = threading.Lock()
        self.containerDrawLock = threading.Lock()
        self.containerUpdateLock = threading.Lock()
        
    def add(self, spr, depth = 0):
        self.containerRenderLock.acquire()
        
        self.m_container.append(spr)
        #spr.__attatch_internal(self)
        
        self.containerRenderLock.release()
        
    def remove(self, spr):
        self.containerRenderLock.acquire()
        self.containerDrawLock.acquire()
        self.containerUpdateLock.acquire()
        
        self.m_container.pop(spr)
        self.__release_internal(self)
        
        self.containerUpdateLock.release()
        self.containerDrawLock.release()
        self.containerRenderLock.release()
    
    def update(self):
        self.containerUpdateLock.acquire()
        
        sprites = self.sprites()
        for spr in sprites:
            spr.update()
        
        self.containerUpdateLock.release()
    
    def render(self):
        self.containerRenderLock.acquire()
        
        sprites = self.sprites()
        for spr in sprites:
            spr.render()
        
        self.containerRenderLock.release()
        
    def draw(self, t_surface):
        self.containerDrawLock.acquire()
        
        sprites = self.sprites()
        for spr in sprites:
            spr.draw(t_surface)
        
        self.containerDrawLock.release()
        
    def sprites(self):
        return self.m_container
    
class SpriteHandler(SpriteGroup):
    def __init__(self, t_window):
        
        SpriteGroup.__init__(self)
        self.m_containerLock = threading.Lock()
        
    def setWindow(self, t_window):
        self.m_window = t_window
    
    def getWindow(self):
        return self.m_window
    
    def handleEvent(self, e):
        self.m_containerLock.lock();
        
        sprites = self.sprites()
        
        if e.type == SDL_MOUSEMOTION:
            
            for spr in sprites:
                
                if (spr.m_mouseOver): # if entered before
                    if ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                        spr.onHover()
                    else:
                    
                        spr.m_mouseOver = False
                        spr.onLeave()
                    
                elif ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                        spr.m_mouseOver = True
                        spr.onEnter()
                        
        if e.type == SDL_MOUSEBUTTONDOWN:

            if (e.button.button == SDL_BUTTON_LEFT):

                for spr in sprites:
                    if ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                        spr.m_pressed = True
                        spr.onPressed()
                    #temp->onClicked();
            
            if (e.button.button == SDL_BUTTON_RIGHT):
                for spr in sprites:
                    if ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                        spr.m_pressed = True
                        spr.onRightClicked()
            
        if e.type == SDL_MOUSEBUTTONUP:

            if (e.button.button == SDL_BUTTON_LEFT): #Change to switch-case statements?
                for spr in sprites:
                    if ( spr.m_pressed ):
                        if m_window.m_mouse.isCollided(spr.m_rect) :
                            spr.m_pressed = False
                            spr.onClicked(); # TODO: refer order from python.
                            spr.onReleased();
                         
                    #temp->onClicked();
        if e.type == SDL_KEYDOWN:
            print ("Physical {} key acting as {} key\n",
                SDL_GetScancodeName(e.key.keysym.scancode),
                SDL_GetKeyName(e.key.keysym.sym));
        if e.type == SDL_KEYUP:
            pass
        
        self.m_containerLock.unlock();

        

        
class SpriteFactory():
    def __init__(self, t_window):
        self.window = t_window
        self.default_args = list()
        
    def create_sprite(self):
        pass
    
    
