import pygame
from widgets import App
from widgets.Button import TextButton, ButtonGroup, create_button_theme
class New(App):
    def __init__(self, eobj):
        App.__init__(self, eobj)
        self.button = TextButton()
       
        self.button.set_theme(create_button_theme("hello", "noooooo", "dooo"), create_button_theme((0, 0, 0)))
        self.button.drect = pygame.Rect((5, 5, 50, 50))
        self.button.clicked(self.prit, ())
    def prit(self):
        print "clicked"
    
    def update(self):
        self.button.update()
    def draw(self, surface):
        self.button.draw(surface)
