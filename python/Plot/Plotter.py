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
from widgets.Plot import Plot
from widgets.Button import TextButton, create_button_theme, ButtonGroup, Button
from widgets.TextField import TextFieldSingleLine
import widgets
from curveFO import curveFvO
from excel_reader import XLSXLoader

STRAIGHT_CURVE = 0
SECOND_DEG_PARABOLA = 1
SINE_WAVE = 2

class Plotter():
    def __init__(self, engineObj):
        
        self.plot_surface = Plot()
        self.plot_surface.rect.x = 40
        self.plot_surface.rect.y = 50
        
        self.button_group = ButtonGroup()
        self.g = engineObj
        
        self.panel = widgets.Panel()
        self.init_buttons()
        
        # Load data from excel and plot.
        self.xlsx = XLSXLoader()
        self.curve = curve = curveFvO()
        curve.loadXYList(self.xlsx.getXYList())
        self.plot_surface.set_f_function(self.curve.function_straight_line_least_square_fitting)
        self.plot_surface.setPoints(self.curve.getPoints())
        #self.plot_surface.hover(self.updateXY,(,))
        self.plot_surface.hover(self.updateXY)
        
    
    def init_buttons(self):
        # Just declaratin of Text buttons.
        pyGOLPlot = TextLine()
        pyGOLPlot.text = "pyGOLEMplot simulating 2*sin(1*x) + 5*sin(8*x)"
        pyGOLPlot.text_color = (140,140,140)
        pyGOLPlot.font_size = 20
        pyGOLPlot.rect.center = 100, 20
        pyGOLPlot.rect.center = 185, 20
        self.pyGOLPlot = pyGOLPlot
        
        pyGOLEM = TextLine()
        pyGOLEM.text = "pyGOLEM"
        pyGOLEM.text_color = (140,140,140)
        pyGOLEM.font_size = 40
        pyGOLEM.rect.center = 720, 600
        self.pyGOLEM = pyGOLEM
        
        bUsing = TextLine()
        bUsing.text = "built using"
        bUsing.text_color = (140,140,140)
        bUsing.font_size = 20
        bUsing.rect.center = 690, 580
        self.bUsing = bUsing
        
        textX = TextLine()
        textX.text = "x = "
        textX.text_color = (140,140,140)
        textX.font_size = 20
        textX.rect.center = 400, 15
        self.text_x = textX
        
        textY = TextLine()
        textY.text = "y = "
        textY.text_color = (140,140,140)
        textY.font_size = 20
        textY._render()
        textY.rect.center = 400,35
        self.text_x, self.text_y = textX, textY
        
        allowed_chars = [str(i) for i in range(0, 10)]
        
        surf = pygame.Surface([9, 9])
        
        textX_value = TextFieldSingleLine(self.panel, "0", (150, 18))
        #textX_value.text = "0"
        self.textX_value = textX_value
        self.textX_value.set_allowed_chars(allowed_chars)
        textX_value.max_display_length = 20
        self.textX_value.rect.center = 500, 15
        self.textX_value.text = "0"
        
        textY_value = TextFieldSingleLine(self.panel, "0", (150, 18))
        self.textY_value = textY_value
        self.textY_value.rect.center = 500, 35
        textY_value.max_display_length = 20
        self.textX_value.text = "0"
        self.textY_value.set_allowed_chars(allowed_chars)
        
        color_theme = create_button_theme((150,150,150), (130,130,130))
        undonecolor_theme = create_button_theme((160,150,150), (150,130,130))
        
        b = TextButton()
        b.set_theme(create_button_theme("Straight Line"), color_theme)
        b.drect = pygame.Rect([600, 100, 150, 20])
        b.clicked(self.changeCurve, (STRAIGHT_CURVE,))
        
        b1 = TextButton()
        b1.set_theme(create_button_theme("Second Deg Parabola"), color_theme)
        b1.drect = pygame.Rect([600, 125, 150, 20])
        b1.clicked(self.changeCurve, (SECOND_DEG_PARABOLA,))
        
        b2 = TextButton()
        b2.set_theme(create_button_theme("Sine wave Curve"), color_theme)
        b2.drect = pygame.Rect([600, 150, 150, 20])
        b2.clicked(self.changeCurve, (SINE_WAVE,))
        self.button_group.add(b)
        self.button_group.add(b1)
        self.button_group.add(b2)
        
    def updateXY(self):
        self.textX_value.text, self.textY_value.text = str(self.plot_surface.xy[0]), str(self.plot_surface.xy[1])
        #self.textX_value.rect = pygame.Rect([430,10, 150, 20])
        #self.textY_value.rect = pygame.Rect([430,30, 150, 20])
    def changeCurve(self, curve_const):
        curve = self.curve
        if curve_const == STRAIGHT_CURVE:
            self.xlsx = XLSXLoader()
            #curve = self.curve
            curve.setFunctionType(STRAIGHT_CURVE)
            self.plot_surface.setRangeX(0, 40, 1)
            self.plot_surface.setRangeY(0, 40, 1)
            curve.loadXYList(self.xlsx.getXYList())
            self.plot_surface.set_f_function(self.curve.function_straight_line_least_square_fitting)
            self.plot_surface.setPoints(self.curve.getPoints())

        if curve_const == SECOND_DEG_PARABOLA:
            self.xlsx = XLSXLoader()
            curve.setFunctionType(SECOND_DEG_PARABOLA)
            curve.loadXYList(self.xlsx.getXYList())
            self.plot_surface.setRangeX(0, 40, 1)
            self.plot_surface.setRangeY(0, 40, 1)
            #self.curve = curve = curveFvO()
            curve.loadXYList(self.xlsx.getXYList())
            self.plot_surface.set_f_function(self.curve.function_second_deg_parabola_least_square_fitting)
            self.plot_surface.setPoints(self.curve.getPoints())
        
        if curve_const == SINE_WAVE:
            #self.xlsx = XLSXLoader()
            self.xlsx = XLSXLoader()
            curve.setFunctionType(SINE_WAVE)
            curve.loadXYList(self.xlsx.getXYList())
            #curve.load()
            self.plot_surface.setRangeX(0, 10, 1)
            #self.plot_surface.setRangeY(-10, 30, 1)
            self.plot_surface.setRangeY(0, 40, 1)
            print "hello"
            self.plot_surface.set_f_function(self.curve.function_sine_wave_fitting)
            self.plot_surface.setPoints(self.curve.getPoints())
        
    def load(self, loadobj):
        pass
        
    def handle_event(self, event):
        self.panel.update(event)
        
    def update(self):
    
        self.plot_surface.update()
        
    def draw(self, surface):
    
        self.plot_surface.draw(surface)
        
        self.button_group.draw(surface)
        self.text_x.draw(surface)
        self.text_y.draw(surface)
        self.textX_value.draw(surface)
        self.textY_value.draw(surface)
        self.pyGOLEM.draw(surface)
        self.bUsing.draw(surface)
        self.pyGOLPlot.draw(surface)
        
