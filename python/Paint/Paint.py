'''
    VERSION: 0.0.3 Curly Legs
    
    Authors: Anantha Krishna R.
'''

"""
    Drawing Surface -> draw the things on this surface.
    Image will copy the drawing surface and blit it to the screen.
    drawing_object - will draw the sprite object over the screen.

"""
import pygame
from pygame.locals import *

from widgets import *

from widgets.Paint import PaintSurface
from widgets.Text import TextLine
import widgets

from widgets.Button import TextButton, create_button_theme, ButtonGroup, Button

class Paint():
    def __init__(self, engineObj):
        
        self.paint_surface = PaintSurface()
        self.paint_surface.rect.x = 40
        self.paint_surface.rect.y = 50
        
        self.g = engineObj
        
        self.init_shape_selection_buttons()
        
        self.shape_text = {
            widgets.Paint.RECTANGLE : "Rectangle",
            widgets.Paint.ELLIPSE : "Ellipse",
            widgets.Paint.LINE : "Line",
            widgets.Paint.CIRCLE : "Circle",
        }
        
    def init_shape_selection_buttons(self):
        
        psurf = self.paint_surface
        
        # Just declaratin of Text buttons.
        tools = TextButton()
        self.dtext = TextLine()
        self.htext = TextLine()
        
        rectangle = TextButton()
        ellipse = TextButton()
        line = TextButton()
        circle = TextButton()
        
        clear = TextButton()
        undo = TextButton()
        redo = TextButton()
        reset = TextButton()
        exit = TextButton()
        
        # Warning: Not exatly supposed to be a button. For DEMO purpose only
        console = Button()
        
        # Setting theme and position.
        color_theme = create_button_theme((150,150,150), (130,130,130))
        undonecolor_theme = create_button_theme((160,150,150), (150,130,130))
        
        tool_color_theme = create_button_theme((180,180,180))
        tools.set_theme(create_button_theme("Tools"), tool_color_theme)
        tools.drect = pygame.Rect([635,60, 150, 20])
        
        self.dtext.text = "Drawing Surface"
        self.dtext.text_color = (140,140,140)
        self.dtext.font_size = 20
        self.dtext.rect = pygame.Rect([240,30, 150, 20])
        
        self.htext.text = "Rectangle"
        self.htext.text_color = (140,140,140)
        self.htext.font_size = 19
        #self.htext.rect = pygame.Rect([600,290, 150, 20])
        
        rectangle.clicked(psurf.change_shape, (widgets.Paint.RECTANGLE,))
        rectangle.set_theme(create_button_theme("Rectange"), color_theme)
        rectangle.drect = pygame.Rect([600,100, 100, 20])
        
        ellipse.clicked(psurf.change_shape, (widgets.Paint.ELLIPSE,))
        ellipse.set_theme(create_button_theme("Ellipse"), color_theme)
        ellipse.drect = pygame.Rect([600,140, 100, 20])
        
        line.clicked(psurf.change_shape, (widgets.Paint.LINE,))
        line.set_theme(create_button_theme("Line"), color_theme)
        line.drect = pygame.Rect([600,180, 100, 20])
        
        circle.clicked(psurf.change_shape, (widgets.Paint.CIRCLE,))
        circle.set_theme(create_button_theme("Circle"), undonecolor_theme)
        circle.drect = pygame.Rect([600,220, 100, 20])
        
        clear.clicked(psurf.clear, ())
        clear.set_theme(create_button_theme("Clear"), color_theme)
        clear.drect = pygame.Rect([710,100, 100, 20])
        
        undo.clicked(psurf.undo, ())
        undo.set_theme(create_button_theme("Undo"), color_theme)
        undo.drect = pygame.Rect([710,140, 100, 20])
        
        redo.clicked(psurf.redo, ())
        redo.set_theme(create_button_theme("Redo"), color_theme)
        redo.drect = pygame.Rect([710,180, 100, 20])
        
        reset.clicked(psurf.reset, ())
        reset.set_theme(create_button_theme("Reset"), color_theme)
        reset.drect = pygame.Rect([710,220, 100, 20])
        
        exit_color_theme = create_button_theme((240,180,180), (170,150,150))
        exit.clicked(self.g.exit, ())
        exit.set_theme(create_button_theme("Exit"), exit_color_theme)
        exit.drect = pygame.Rect([710,260, 100, 20])
        #self.line.clicked(psurf.change_shape, (widgets.Paint.LINE))
        
        surf = pygame.Surface((220,180)).convert()
        surf.fill((20,20,20))
        console.theme = create_button_theme(surf)
        console.rect = pygame.Rect([600,350, 220, 180])
        
        # Adding to container.
        self.button_group = ButtonGroup()
        self.button_group.add([tools])
        self.button_group.add([rectangle, ellipse, line, circle])
        self.button_group.add([clear, undo, redo, reset, exit])
        self.button_group.add(console)
        
        self.actions = {
            K_r : rectangle,
            K_e : ellipse,
            K_l :line ,
            K_c : circle,
            frozenset([K_LSHIFT, K_c]) : clear,
            frozenset([K_LCTRL, K_z]) : undo,
            frozenset([K_LCTRL, K_LSHIFT, K_z]) : redo,
            frozenset([K_LCTRL, K_r]) : reset,
        }
        
    def load(self, loadobj):
        pass
        
    def handle_event(self, event):
        pass
        
    def update(self):
    
        self.paint_surface.update()
        
        self.htext.text = self.shape_text[self.paint_surface.current_shape]
        callback = None
        key = pygame.key.get_pressed()

        if key[K_LSHIFT] and key[K_c]: callback = self.actions[frozenset([K_LSHIFT, K_c])]
        if key[K_LCTRL] and key[K_z]: callback = self.actions[frozenset([K_LCTRL, K_z])]
        if key[K_LCTRL] and key[K_LSHIFT] and key[K_z]: callback = self.actions[frozenset([K_LCTRL, K_LSHIFT, K_z])]
        if key[K_LCTRL] and key[K_r]: 
            callback = self.actions[frozenset([K_LCTRL, K_r])]
        
        if callback:
            callback.on_event("start_clicked")
            callback.on_event("pressed")
        
    def draw(self, surface):
    
        self.paint_surface.draw(surface)
        
        self.button_group.draw(surface)
        self.dtext.draw(surface)
        self.htext.draw(surface)
