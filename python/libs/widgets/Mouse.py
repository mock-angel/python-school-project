# Mouse.py
import pygame

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        
        self.image = pygame.Surface([1, 1])
        self.image.fill((5,50,255))
        
        #self.mask = pygame.mask.from_surface(self.image)
        (self.point) = self.rect = self.image.get_rect()
        self.update()
        
    def update(self):
        (self.point) = (self.rect.x, self.rect.y) = pygame.mouse.get_pos()
        #self.mask = pygame.mask.from_surface(self.image)
        
    def get_pos(self):
        return self.rect.x, self.rect.y
    
    def changed_state(self):
        return False
