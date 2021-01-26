# TitleBar.py
import pygame

from widgets.Button import Button, ButtonGroup, create_button_theme

class close_button(Button):
    def __init__(self, panel, engine):
        super(close_button, self).__init__(panel)
        
        self.theme = create_button_theme(pygame.image.load("data/themes/default/titlebar/close.png").convert())

        self.rect = self.image.get_rect()
        self.rect.right = 915 - 5
        
        self.clicked(engine.exit, ())
        
class iconify_button(Button):
    def __init__(self, panel):
        super(iconify_button, self).__init__(panel)
        
        self.theme = create_button_theme(pygame.image.load("data/themes/default/titlebar/iconify.png").convert())
        
        self.rect = self.image.get_rect()
        self.rect.right = 915 - 5 - 15
        
        self.clicked(self.iconify, ())
        
    def iconify(self):
        pygame.display.iconify()

class title_bar(Button):
    def __init__(self, panel=None):
        super(title_bar, self).__init__(panel)
        
        self.theme = create_button_theme(pygame.image.load("data/themes/default/titlebar/title_bar.png").convert())
        
        self.rect = self.image.get_rect()
        

class TitleBar(ButtonGroup):
    def __init__(self, engine ,panel=None):
        super(TitleBar, self).__init__()
        self.title_bar = title_bar(panel)
        
        self.add(iconify_button(panel))
        self.add(close_button(panel, engine))
    def draw(self, surface):

        surface.blit(self.title_bar.image, (0, 0))
        super(TitleBar, self).draw(surface)
