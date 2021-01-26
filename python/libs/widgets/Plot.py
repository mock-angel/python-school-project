# Paint.py
import pygame

from Mouse import Mouse
from Button import Button, create_button_theme
import numpy as np
RECTANGLE = 0
SQUARE = 1
ELLIPSE = 2
CIRCLE = 3
LINE = 4
SURFACE = -1

QUADRANT1 = 0
QUADRANT2 = 1
QUADRANT3 = 2
QUADRANT4 = 3
QUADRANTFULL = 4
        
class Plot(Button):
    def __init__(self, size = (500, 500)):
        Button.__init__(self)
        self.size = size
        self.plot_type = QUADRANT1
        self.set_f_function(self.dummy_f)
        
        self.point_color = 0, 0, 205 # 0, 0, 255
        self.plot_color = 205, 0, 0 # 255, 0, 0
        self.xy = 0, 0
        self.init_plotsurfaces()
        
    def init_plotsurfaces(self):
        """Init code."""
        
        self.drawing_surface = pygame.Surface(self.size).convert()
        self.drawing_surface.fill((200,200,200))
        self.image = self.drawing_surface.copy()
        
        self.theme = create_button_theme(self.image)
        
        cdefault = pygame.cursors.arrow
        chov = pygame.cursors.broken_x
        
        self.cursors = create_button_theme(cdefault, chov)
        
        self.draw_color = (100,100,100)
        self.rect = self.image.get_rect()
        
        self.points_list = []
        self.y_axis = (0, 0), (0, 0), 2
        self.x_axis = (0, 0), (0, 0), 2
        if self.plot_type == QUADRANT1:
            self.y_axis = (40,40), (40, self.size[1]-40)
            self.x_axis = (40,self.size[1]-40), (self.size[0]-40, self.size[1]-40)
            self.y_axis_right = (self.size[0]-40,40), (self.size[0]-40, self.size[1]-40)
            self.x_axis_top = (40,40), (self.size[0]-40, 40)
            self.start_x = 40
            self.start_y = self.size[1]-40
            self.end_x = self.size[0]-40
            self.end_y = 40
            
            self.range_value_x = 0, 60, 1
            self.range_value_y = 0, 60, 1
            
            self.screen_x_len = screen_x_len = float((self.size[0]-40)-40)
            self.screen_y_len = screen_y_len = float((self.size[1]-40)-40)
            #x_list = range(r_x[0], r_x[1], 1.0/r_x[0])
            self.x_step = float(self.range_value_x[1] - self.range_value_x[0])/screen_x_len
            self.y_step = float(self.range_value_y[1] - self.range_value_y[0])/screen_y_len
    
    def setRangeX(self, xs, xe, xp):
        self.range_value_x = xs, xe, xp
        self.x_step = float(self.range_value_x[1] - self.range_value_x[0])/float(self.screen_x_len)

    def setRangeY(self, ys, ye, yp):
        self.range_value_y = ys, ye, yp
        self.y_step = float(self.range_value_y[1] - self.range_value_y[0])/float(self.screen_y_len)
        
    def clear(self):
        """Clears the plot.
        """
        pass 
                   
    def update(self):
        pass
    
    def set_f_function(self, callback):
        self.f_function = callback
        pass
    
    
    
    def dummy_f(self, x):
        #equation y = x
        return x
    
    def draw_curve(self, surface):
        r_x = self.range_value_x
        r_y = self.range_value_y
        
        prev_x = r_x[0]
        prev_y = self.f_function(prev_x)
        
        curr_x = r_x[0]
        curr_y = prev_y
        
        start_x, start_y = self.start_x, self.start_y
        end_x, end_y = self.end_x, self.end_y
        
        x_step, y_step = self.x_step, self.y_step
        while (True):
            curr_x += x_step
            if curr_x < r_x[0] or curr_x > r_x[1]: break
            curr_y = self.f_function(curr_x)
            
            # TODO FIXME:
            if curr_y == 0: 
                prev_x = curr_x
                prev_y = curr_y
                continue
            
            #if curr_y < r_y[0] or curr_y > r_y[1]: continue
            if curr_y > r_y[1]: continue
            line = ((prev_x- self.range_value_x[0])/x_step+40, self.size[1] - (prev_y- self.range_value_y[0])/y_step - 40), ((curr_x- self.range_value_x[0])/x_step+40, self.size[1] - (curr_y- self.range_value_y[0])/y_step - 40), 2
            pygame.draw.line(surface, self.plot_color, *line)
            prev_x = curr_x
            prev_y = curr_y
        return
        while(True):
            if (start_x<end_x): # increment x
                if curr_x+1<=end_x: curr_x += 1
                else: break
            if (start_x>end_x): # decrement x
                if curr_x-1>=end_x: curr_x -= 1
                else: break
            
            curr_y = self.size[1] - self.f_function(curr_x)
            
            """if (s_xy[1]<e_xy[1]): # incremental y
                if curr_y<=e_xy[1]: pass
                else: break
            
            if (s_xy[1]<e_xy[1]): # decrement x
                if curr_y<=e_xy[1]: pass
                else: break
            """
            if curr_y<40 or curr_y>self.size[1]-40: continue
            
            line = (prev_x, prev_y), (curr_x, curr_y), 2
            pygame.draw.line(surface, self.draw_color, *line)
            #print curr_x, curr_y
            prev_x = curr_x
            prev_y = curr_y
    
    def draw_marker(self, surface):
        #- self.range_value_x[0] for m_x
        m_xy = self.mouse_xy
        m_x = m_xy[0] - self.rect.x
        m_y = m_xy[1] - self.rect.y
        if (m_x<40 or m_x>self.size[0] - 40): return
        if (m_y<40 or m_y>self.size[1] - 40): return
        
        line_y = (m_x, 40), (m_x, self.size[1] - 40), 1
        line_x = (40, m_y), (self.size[0] - 40, m_y), 1
        
        #pygame.draw.line(surface, self.draw_color, *line_y)
        #pygame.draw.line(surface, self.draw_color, *line_x)
        
        x_step, y_step = self.x_step, self.y_step
        x, y = (m_x - 40) * x_step, (m_y - 40) * y_step
        
        f_y = self.f_function(x)
        self.xy = x, f_y
        if self.size[1] - (f_y)/y_step - 40<40: return
        #print x, f_y #  <- x and y
        line_y = (m_x, 40), (m_x, self.size[1] - 40), 1
        line_x = (40, self.size[1] - (f_y- self.range_value_y[0])/y_step - 40), (self.size[0] - 40, self.size[1] - (f_y- self.range_value_y[0])/y_step - 40), 1
        pygame.draw.line(surface, self.draw_color, *line_y)
        pygame.draw.line(surface, self.draw_color, *line_x)
        
        
    def draw_axes(self, surface):
        
        pygame.draw.line(surface, self.draw_color, *self.y_axis)
        pygame.draw.line(surface, self.draw_color, *self.x_axis)
        pygame.draw.line(surface, self.draw_color, *self.y_axis_right)
        pygame.draw.line(surface, self.draw_color, *self.x_axis_top)
        r_x = self.range_value_x
        r_y = self.range_value_y
        
        #o_step_x = float(r_x[1] - r_x[0])/r_x[2]
        #o_step_y = float(r_y[1] - r_y[0])/r_y[2]
        
        line_x_list = []
        line_y_list = []
        x_list = np.linspace(r_x[0], r_x[1], num=(r_x[2]*(r_x[1] - r_x[0])))
        y_list = np.linspace(r_y[0], r_y[1], num=(r_y[2]*(r_y[1] - r_y[0])))
        
        for x in x_list:
            line_x_list.append([((x/self.x_step)+40, self.size[1] - 35), ((x/self.x_step)+40, self.size[1] - 45), 1])
            line_x_list.append([((x/self.x_step)+40, 35), ((x/self.x_step)+40, 45), 1])
        
        for y in y_list:
            line_y_list.append([(self.size[0] - 35, (y/self.y_step)+40), (self.size[0] - 45, (y/self.y_step)+40), 1])
            line_y_list.append([(35, (y/self.y_step)+40), (45, (y/self.y_step)+40), 1])
        
        for line_x in line_x_list:
            pygame.draw.line(surface, self.draw_color, *line_x)
        for line_y in line_y_list:
            pygame.draw.line(surface, self.draw_color, *line_y)
        
        temp_line = (40,self.size[1]-40 + self.range_value_y[0]/self.y_step), (self.size[0]-40, self.size[1]-40+ self.range_value_y[0]/self.y_step)
        #temp_line = (((x)/self.x_step)+40, self.size[1] - 35), ((x/self.x_step)+40, self.size[1] - 45), 1
        
        pygame.draw.line(surface, self.draw_color, *temp_line)# remove this.
    def setPoints(self, points_list):
        self.points_list = points_list
        for xy in self.points_list:
            x = xy[0]
        
    def draw_points(self, surface):
        line_list = []
        s_x, s_y = self.size[0], self.size[1]
        for point in self.points_list:
            x, y = (point[0]- self.range_value_x[0])/self.x_step, s_y - (point[1]- self.range_value_y[0])/self.y_step
            line_list.append([(x+33, y - 40), (x+47, y - 40), 1])
            line_list.append([(x+40, y - 33), (x+40, y - 47), 1])
            line_list.append([(x+35, y - 35), (x+45, y - 45), 1])
            line_list.append([(x+45, y - 35), (x+35, y - 45), 1])
            
            
        for line in line_list:
            pygame.draw.line(surface, self.point_color, *line)
            
    def draw(self, surface):
        """draw() draws all the shapes in order of their creation."""
        
        self.draw_axes(self.image)
        self.draw_marker(self.image)
        self.draw_curve(self.image)
        self.draw_points(self.image)
        
        # The drawing screen background.
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        self.image.fill((200,200,200))
        
