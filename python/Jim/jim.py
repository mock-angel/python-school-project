'''
    VERSION: 0.0.2 Creepy Arms
    
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
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QListWidget, QComboBox, QLabel, QTabWidget, QGridLayout, QCheckBox, QFrame, QStyleFactory, QDateEdit, QScrollBar, QTableWidget, QTableWidgetItem, QHBoxLayout
STRAIGHT_CURVE = 0
SECOND_DEG_PARABOLA = 1
SINE_WAVE = 2
from excel_reader import XLSXLoader
from JimProgram import JimMain
from threading import Thread

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class JimDialogue(Gtk.Dialog):

    def __init__(self, parent = None, text = None):
        Gtk.Dialog.__init__(self, "Region Info", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("This is where the information is displayed" if text == None else text)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class Jim():
    def __init__(self, engineObj):
        
        self.plot_surface = Plot()
        self.plot_surface.rect.x = 40
        self.plot_surface.rect.y = 50
        
        self.button_group = ButtonGroup()
        self.g = engineObj
        
        self.panel = widgets.Panel()
        self.init_buttons()
        
        self.x = 0
        #self.points = [(6, 36.5), (7, 37), (8,40)]
        # Load data from excel and plot.
        self.xlsx = XLSXLoader()
        self.curve = curve = curveFvO()
        #curve.loadXYList(self.xlsx.getXYList())
        self.plot_surface.set_f_function(self.plotting_method_f)
        #self.plot_surface.setPoints(self.points)
        #self.plot_surface.hover(self.updateXY,(,))
        self.plot_surface.hover(self.updateXY)
        self.plot_surface.clicked(self.msgbxProcess)
        
        
        self.xlsWorker = XLSXLoader()
        self.data = self.xlsWorker.data
        self.updatePoints(self.data)
        
        self.JU = JimMain
        self.t = t = Thread(target=self.JU, args=(self, ) )
        t.start()
        
    def plotting_method_f(self, x):
        y = 0
        data = self.data
        l = range(len(data) - 1)
        for i in l:
            if data[i].t<=x and data[i+1].t>x:
                y = ((data[i+1].k - data[i].k)/float(data[i+1].t - data[i].t))*(x - data[i+1].t) + data[i+1].k
                return y
        return y
    
    def msgbxProcess(self):
        text = """Data at Time {0}      Data at Time {1}
<h3>Changes:</h3>
 * Designed a very consistant and reliable table to handle item input.<br/>
 * The total is now converted to words.<br/>
 * Added a few buttons to adding/ editing or deleting a customer seamlessly in database possible.<br/>
 * Made connection to database an option during start of the program.<br/>
 * The program is made compatible for both offline and online modes.<br/>
 * Fixed error AttributeError during close of a program when not connected to internet database.<br/>
 * Changed the code design for option handling and collecting (Meaning: The item sets in table are not maintained by Machine Name anymore, instead their Item number).<br/>
<h3>Known Problems/Bugs:</h3>
 * None currently<br/>
 <br/>
<h4>INVm-0.0.4.2 (Upcoming version)</h4>
<h3>What to expect:</h3>
 * A way to calculate Deference automatically.
""".format('3','4')
        x = self.x
        
        data = self.data
        Fdata = Pdata = None
        for i in range(len(data)):
            if (data[i].t >= x):
                print data[i].t, x
                Fdata = data[i]
                Pdata = data[(i-1) if i-1>0 else 0 ]
                break
        if Fdata == None: Fdata, Pdata = data[-1], data[-2]
        text = """For Data at time\t{0:6}\n
Data b/w Time:\t{1:>6}       to      {2:>6}\n
Temp:\t\t\t\t{3:>6}       {4:>6}\n
BPM:\t\t\t\t{5:>6}               {6:>6}\n
Sweat Rate:\t\t{7:>6}               {8:>6}

""".format(self.x, str(Pdata.t)+" s", str(Fdata.t)+" s",
                    str(Pdata.k)+" deg", str(Fdata.k)+" deg",
                    Pdata.bpm, Fdata.bpm,
                    Pdata.spm, Fdata.spm)
        d = JimDialogue(None, text)
        #d.connect("destroy", Gtk.main_quit)
        #d.add_buttons(Gtk.STOCK_OK, 1)
        
        answer = d.run()
        d.destroy()
        
        print(answer)
    def init_buttons(self):
        # Just declaratin of Text buttons.
        pyGOLPlot = TextLine()
        pyGOLPlot.text = "pyGolemJim"
        pyGOLPlot.text_color = (140,140,140)
        pyGOLPlot.font_size = 30
        pyGOLPlot.rect.center = 100, 20
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
        
        #b = TextButton()
        #b.set_theme(create_button_theme("Straight Line"), color_theme)
        #b.drect = pygame.Rect([600, 100, 150, 20])
        #b.clicked(self.changeCurve, (STRAIGHT_CURVE,))
        
        #b1 = TextButton()
        #b1.set_theme(create_button_theme("Second Deg Parabola"), color_theme)
        #b1.drect = pygame.Rect([600, 125, 150, 20])
        #b1.clicked(self.changeCurve, (SECOND_DEG_PARABOLA,))
        
        #b2 = TextButton()
        #b2.set_theme(create_button_theme("Sine wave Curve"), color_theme)
        #b2.drect = pygame.Rect([600, 150, 150, 20])
        #b2.clicked(self.changeCurve, (SINE_WAVE,))
#        self.button_group.add(b)
#        self.button_group.add(b1)
#        self.button_group.add(b2)
        
    
    def save(self):
        self.xlsWorker.save()
    
    def __delete__(self):
        self.t.join()
        print("joined")
    def updateXY(self):
        pass
        self.textX_value.text, self.textY_value.text = str(self.plot_surface.xy[0]), str(self.plot_surface.xy[1])
        self.textX_value.rect = pygame.Rect([430,10, 150, 20])
        self.textY_value.rect = pygame.Rect([430,30, 150, 20])
        
        self.x = self.plot_surface.xy[0]
        self.y = self.plot_surface.xy[1]
#    def changeCurve(self, curve_const):
#        curve = self.curve
#        if curve_const == STRAIGHT_CURVE:
#            self.xlsx = XLSXLoader()
#            #curve = self.curve
#            curve.setFunctionType(STRAIGHT_CURVE)
#            self.plot_surface.setRangeX(0, 40, 1)
#            self.plot_surface.setRangeY(0, 40, 1)
#            curve.loadXYList(self.xlsx.getXYList())
#            self.plot_surface.set_f_function(self.curve.function_straight_line_least_square_fitting)
#            self.plot_surface.setPoints(self.curve.getPoints())

#        if curve_const == SECOND_DEG_PARABOLA:
#            self.xlsx = XLSXLoader()
#            curve.setFunctionType(SECOND_DEG_PARABOLA)
#            self.plot_surface.setRangeX(0, 40, 1)
#            self.plot_surface.setRangeY(0, 40, 1)
#            #self.curve = curve = curveFvO()
#            curve.loadXYList(self.xlsx.getXYList())
#            self.plot_surface.set_f_function(self.curve.function_second_deg_parabola_least_square_fitting)
#            self.plot_surface.setPoints(self.curve.getPoints())
#        
#        if curve_const == SINE_WAVE:
#            #self.xlsx = XLSXLoader()
#            curve.setFunctionType(SINE_WAVE)
#            curve.load()
#            self.plot_surface.setRangeX(0, 10, 1)
#            self.plot_surface.setRangeY(-10, 30, 1)
#            
#            self.plot_surface.set_f_function(self.curve.function_sine_wave_fitting)
#            self.plot_surface.setPoints(self.curve.getPoints())
    
    def updatePoints(self, dataList):
        points = []
        for i in dataList:
            x, y = i.t, i.k
            points.append((x, y), )
        
        self.plot_surface.setPoints(points)
    
    def insert_data(self, data):
        
        self.xlsWorker.inputData(data)
        dataList = self.xlsWorker.data
        self.updatePoints(dataList)
        self.data = dataList
        
        
#        self.sort()
    
#    def sort():
#        d = self.data
#        lowestX = 999999999999999
#        lObj = None
#        refList = []
#        for c in range len(d)
#            for i in d:
#                if i.x < lowestX:
#                    lowestX = i.t
#                    lObj = i
#            refList.append(lObj)
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
        
