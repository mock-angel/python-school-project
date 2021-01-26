# Clock.py
import math
from calendar import monthrange as mr
from datetime import datetime

import pygame

from Text import TextLine

draw_circle = pygame.draw.circle
draw_line = pygame.draw.line

class ClockEssentials():
    time_captured = None
    
    ########################################################################
    # Needle.
    @staticmethod
    def get_rough_angles():
        
#        Old and heavy but very fast.
#        h_a = math.radians(((time_now.hour%12) / 12.) * 360)
#        m_a = math.radians((time_now.minute / 60.) * 360)
#        s_a = math.radians((time_now.second / 60.) * 360)

        hh, mm, ss = ClockEssentials.get_rough_hms()
        
        h_a = math.radians(-1 * ( (hh * 360) - 90))
        m_a = math.radians(-1 *( (mm * 360) - 90))
        s_a = math.radians(-1 *( (ss * 360) - 90))
        
        return h_a, m_a, s_a
    
    @staticmethod
    def get_smooth_angles():
        """get_smooth_angles() Converts hms in range 0-1 to angles 
        and then to xy coords."""
        
        time_now = ClockEssentials.time_captured
        
        hh, mm, ss = ClockEssentials.get_smooth_hms()
        
        h_a = math.radians(-1 * ( (hh * 360) - 90))
        m_a = math.radians(-1 *( (mm * 360) - 90))
        s_a = math.radians(-1 *( (ss * 360) - 90))
        
        return h_a, m_a, s_a
    
    ########################################################################
    # HMS Fraction b/w range 0-1.
    @staticmethod
    def get_rough_hms():
        """get_rough_hms() - returns hms b/w range 0-1 in step fashion."""
        
        time_now = ClockEssentials.time_captured
        
        h = (time_now.hour%12) / 12.
        m = (time_now.minute / 60.)
        s = (time_now.second / 60.)
        
        return h, m ,s
        
    @staticmethod
    def get_smooth_hms():
        """get_smooth_hms() - returns hms b/w the range 0-1 in smooth fashion, 
        i.e high precision."""
        
        time_now = ClockEssentials.time_captured
        
        microsecond = time_now.microsecond/1000000.
        second = (time_now.second / 60.) + (microsecond if microsecond<1 else 0)/60.
        minute = (time_now.minute / 60.) + (second if second<1 else 0)/60.
        hour = ((time_now.hour%12 ) / 12.) + (minute if minute<1 else 0)/12.
        return hour, minute, second
    
    
    @staticmethod
    def get_rough_dmy():
        """get_rough_hms() - returns hms b/w range 0-1 in step fashion."""
        
        
        time_now = ClockEssentials.time_captured
        
        h, m, s = ClockEssentials.get_rough_hms()
        
        D = time_now.day # TODO: convert day to fraction b/w range 0-1.
        M = (time_now.month / 12.)
        Y = (time_now.year)
        
        return D, M, Y
    
    @staticmethod
    def get_smooth_dmy():
        # TODO: Pleae work on this one at a later stage?.
        
        """get_rough_hms() - returns hms b/w range 0-1 in step fashion."""
        
        
        time_now = ClockEssentials.time_captured
        
        h, m, s = ClockEssentials.get_smooth_hms()
        
        D = time_now.day # TODO: convert day to fraction b/w range 0-1.
        M = (time_now.month / 12.) + float(D)/mr(time_now.year, time_now.month)[1]
        Y = (time_now.year)
        
        return D, M, Y
    
    @staticmethod
    def capture_time():
    
        ClockEssentials.time_captured = datetime.now()
    
class Clock():
    # A test math clock.
    # A program can just use the update method and get the coordinates of all hands.
    
    def __init__(self):
        
        self.radius = 100
        self.radius_tuple = (40, 70, 80)
        
        sec_needle_color = (255, 100, 100)
        min_needle_color = (55, 35, 53)
        hour_needle_color = (40, 40, 40)
        self.color_tuple = (hour_needle_color, min_needle_color, sec_needle_color)
        
        self.smooth_needle = True
        
        self.fill = False
        
        
        self.center = (0, 0)
        self.clock_color = (145,176,202)
        
                          #  1.1 1.2 1.3 text
        self.lable_radius = (98, 94, 90, 82, 73  )
        
        self.lable_no = 0
        self.max_lable_count = 3
        
        self.init_lables()
        
        self.make_needle_rough()
        
    def init_lables(self):
        self.text_lables_1 = []
        
        
        
        center = 20/2, 20/2
        
        surf = pygame.Surface((20, 20)).convert_alpha()
        surf.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MIN)
        
        rotate = pygame.transform.rotate
        text_color = 68, 78, 55
        
        surf_list = (surf_1, surf_2, surf_3, surf_4, surf_5, surf_6, 
        surf_7, surf_8, surf_9, surf_10, surf_11, surf_12) = (
                    surf.copy(), surf.copy(), 
                    surf.copy(), surf.copy(), surf.copy(), 
                    surf.copy(), surf.copy(), surf.copy(), surf.copy(), surf.copy(),
                    surf.copy(), surf.copy()
        )
        
        text = TextLine()
        text.text_color = text_color
        roman_text_list = ("I", "II", "III", "IV", "V", "VI", 
                            "VII", "VIII", "IX", "X", "XI", "XII")
        
        self.first_surface_list = []
        self.second_surface_list = []
        self.third_surface_list = []
        
        # Create text surfaces.
        for i in range(1, 13):
            text.text = roman_text_list[i-1]
            text.rect.center = center
            text.draw(surf_list[i-1])
            
            # Normal straight text surface.
            text_surf = i, surf_list[i-1].convert_alpha()
            
            # Rotated text surface by a certain angle to the center of the clock.
            text_surfr =  i, rotate(text_surf[1], (12 - i/12.)*360).convert_alpha()
            
            if i in (6, 12):
                self.first_surface_list.append(text_surf)
                self.second_surface_list.append(text_surfr)
                
                self.third_surface_list.append(text_surfr)
            else:
                self.third_surface_list.append(text_surfr)
        
        self.hour_hand_xy = self.min_hand_xy = self.sec_hand_xy = self.center
    def update(self):
        
        ClockEssentials.capture_time() # Capture current time.
        
        h_r, m_r, s_r = self.radius_tuple
        cx, cy = self.center
        
        h_a, m_a, s_a = ClockEssentials.get_smooth_angles() if self.smooth_needle else ClockEssentials.get_rough_angles()
        
        self.hour_hand_xy = cx + h_r * math.cos(h_a), cy + h_r * math.sin(h_a) * -1
        self.min_hand_xy = cx + m_r * math.cos(m_a), cy + m_r * math.sin(m_a) * -1
        self.sec_hand_xy = cx + s_r * math.cos(s_a), cy + s_r * math.sin(s_a) * -1
        
    def set_center(self, center):
        self.center = center
    
    def set_needle_radius(self, radius_tuple):
        
        self.radius_tuple = radius_tuple
    
    def set_needle_color(self, color_tuple):
        self.color_tuple = color_tuple
        
    def get_hms_coords(self):
        return self.hour_hand, self.min_hand, self.sec_hand
    
    def get_hms(self):
        ress = ClockEssentials
        return ress.get_smooth_hms() if self.smooth_needle else ress.get_rough_hms()
    def get_DMY(self):
        ress = ClockEssentials
        return ress.get_smooth_dmy() if self.smooth_needle else ress.get_rough_dmy()
    def make_needle_smooth(self):
        self.smooth_needle = True
    
    def make_needle_rough(self):
        self.smooth_needle = False
    
    # Can be ignored.
    def draw(self, surface):
        
        # Draw clock.
        draw_circle(surface, self.clock_color, self.center, self.radius, 0 if self.fill else 1)
        
        _1, _2, _3, _4, _5 = self.lable_radius
        cx, cy = self.center
        
        # Draw Bars.
        for t in range(60):
            rad_t = math.radians((t/60.)*360 - 90)
            p_1 = cx + _1 * math.cos(rad_t), cy + _1 * math.sin(rad_t)
            p_2 = cx + _2 * math.cos(rad_t), cy + _2 * math.sin(rad_t)
            
            draw_line(surface, (0, 0, 0), p_1, p_2, 1)
            
        for t in range(12):
            rad_t = math.radians((t/12.)*360  - 90)
            p_1 = cx + _1 * math.cos(rad_t), cy + _1 * math.sin(rad_t)
            p_3 = cx + _3 * math.cos(rad_t), cy + _3 * math.sin(rad_t)
            
            draw_line(surface, (0, 0, 0), p_1, p_3, 3)
        
        for t in range(4):
            rad_t = math.radians((t/4.)*360  - 90)
            p_1 = cx + _1 * math.cos(rad_t), cy + _1 * math.sin(rad_t)
            p_4 = cx + _4 * math.cos(rad_t), cy + _4 * math.sin(rad_t)
            
            draw_line(surface, (0, 0, 0), p_1, p_4, 3)
        
        # Draw modes like text and other extras.
        if self.lable_no:
        
            if self.lable_no == 1: li = self.first_surface_list
            if self.lable_no == 2: li = self.second_surface_list
            if self.lable_no == 3: li = self.third_surface_list
            
            for surface_tu in li:
                
                rad_t = math.radians((surface_tu[0]/12.)*360  - 90)
                
                p_1 = cx + _1 * math.cos(rad_t), cy + _1 * math.sin(rad_t)
                
                if surface_tu[0] in ( 6, 9, 12):
                    _ = _5
                    
                elif surface_tu[0] == 3:
                    _ = _5 - 23
                    
                else:
                    _ = _4
                
                p_5 = cx + _ * math.cos(rad_t), cy + _ * math.sin(rad_t)
                p_5_c = p_5[0] - 10, p_5[1] - 10
                
                surface.blit(surface_tu[1], p_5_c)
                
        else: pass
        
        
        # Draw h, m, s needles.
        draw_line(surface, self.color_tuple[0], self.center, self.hour_hand_xy, 2)
        draw_line(surface, self.color_tuple[1], self.center, self.min_hand_xy, 2)
        draw_line(surface, self.color_tuple[2], self.center, self.sec_hand_xy, 2)

class Leaf():
    def __init__(self, size_per_box, _list):
        
        box_count = len(_list)
        
        b_c, size = box_count, size_per_box
        width, height = size, (b_c+2) * size
        
        self.size = size
        self.length = box_count
        
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect((0, 0, size, size * 2))
        self.cropped_rect = self.rect.copy()
        
        self.apply_to_image(_list)
        self.readjust_crop((5/12.)*100)
    def apply_to_image(self, _list):
        size = self.size
        
        rect = pygame.Rect((0, 0, size, size))
        surf = self.image
        
        self.text = TextLine(text="")
        
        i = -1
        for index in range(-1, len(_list)) + [0]:
            self.text.text = _list[index]
            self.text.rect.center = size/2, size/2 +size * (i + 1)
            self.text.draw(surf)
            i+=1
    
    def readjust_crop(self, percentage):
        perone = (percentage/100.) if percentage else 1 # Helps set anim.
        
        pointer_height = (self.length * self.size) * perone - self.size/2
        self.cropped_rect.y = pointer_height
        
    def draw(self, surface):
        
        surface.blit(self.image, self.rect, self.cropped_rect)
