# TextField.py
import time
import pygame

from Panel import Panel
from Text import AbstractTextLine, TextLine

from Button import Button, create_button_theme
from Mouse import Mouse


class LMRTextLine(AbstractTextLine): # Node.
    cursor_surface = None
    
    def __init__(self, initial_string = ""):
        AbstractTextLine.__init__(self)
        
        # Position and size variables.
        self.from_pos = 0
        self.max_display_length = 20
        self.max_stored_length = 0
        
        # Properties.
        self.excess_delete = True
        
        self.allowed_chars = None
        self.allowed_values = None
        
        self.blocked_chars = None
        
        self.restricted_values = None
        # Used to store excess text.
        self.exceeded_string = ""
        
        # Stores the entire string.
        self._stored_string = initial_string
        
        self.new_line = False
        self.back_space_skipped = 0
        
        self.field_group = None
        
        # Vars to make keydowns repeat after user pressed a key for some time:
        #{event.key: (counter_int, event.unicode)} (look for "***") : not implemented.
        self.keyrepeat_counters = {} 
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms = 400
        self.keyrepeat_interval_ms = repeat_keys_interval_ms = 35
        
        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        cursor_color = (0,0, 0)
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(self.stored_string)  # Inside text
        self.cursor_visible = False # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500 # /|\
        self.cursor_ms_counter = 0
        
        self.previous_time  = self.current_time = time.time()
        self.clock = pygame.time.Clock()
        
        self.insert = False # Does both delete and add
        
        self.prev_obj = None
        self.next_obj = None
        
        self.keyboard_focus = True
        
        self.on_return_callback = self.return_event
        self.on_return_params = ()
        
    # Getter.
    ####################################################################################
    @property
    def stored_string(self):
        return self._stored_string
    
    @property
    def cursor_position(self):
        return self._cursor_position
    
    def is_newline(self):
        return self.new_line
        
    
    def get_excess_string(self):
        """get_excess_string() - returns the string when exceeded limit and clears it."""
        
        ex = self.exceeded_string
        self.exceeded_string = ""
        return ex
        
    def get_text_pos_from_x_coord(self, x):
        """get_text_pos_from_x_coord() - gets the coords of the cursor position
        when the mouse is clicked."""
        # TODO: Modify this.
        
        i = 0
#        for i in range(len(self.text)):
#            sx, sy = self.get_size(self.text[:i])
#            if sx > x:
#                i -= 1
        return i
    
    # Setter.
    ####################################################################################
    @stored_string.setter
    def stored_string(self, string):
        
        if not (self.max_stored_length in (None, 0)): 
            self._stored_string = string[0:self.max_stored_length]
            self.exceeded_string = string[self.max_stored_length:] +self.exceeded_string
            
        else:
            self._stored_string = string
            
        self.slice_text()
        self.cursor_position = self._cursor_position
        
        self.string_changed()
    
    # Must be derived. Is called after every change to text.
    def string_changed(self): pass
    
    @cursor_position.setter
    def cursor_position(self, pos):
        
        # TODO: Optimise.
        
        max_display_length = self.max_display_length
        
        if len(self.stored_string) - self.from_pos < self.max_display_length:
            self.from_pos = len(self.stored_string) - max_display_length
            if self.from_pos < 0: self.from_pos = 0
            
        elif pos < self.from_pos:
            self.from_pos = pos
            
        elif pos > self.from_pos + max_display_length:
            self.from_pos = pos - max_display_length
        
        self._cursor_position = pos
        self.slice_text()
    
    def set_allowed_chars(self, seq):
        self.allowed_chars = seq
    
    def set_allowed_values(self, seq):
        self.allowed_values = seq
    
    def set_blocked_chars(self, seq):
        self.blocked_chars = seq
    
    def do_not_delete_exceed(self):
        self.excess_delete = False
        
    def make_newline(self):
        
        self.new_line = True
    
    def set_string(self, string):
        self.stored_string = string
    
    def set_max_char_length(self, length):
        self.max_stored_length = length
    
    # Other.
    def add_text_to_pos(self, text_to_insert, pos):
        self.stored_string = self.stored_string[:pos] + text_to_insert\
                                                     + self.stored_string[pos:]
        
    def on_return(self):
        """Make newline."""
        
        self.on_return_callback(*self.on_return_params)
    
    # Default callback.
    def return_event(self, objFeed = None):
        """Add new object to the chain after this object and before the next object."""
        
        if objFeed: 
            obj = objFeed()
            obj.prev_obj = self
            obj.next_obj = self.next_obj
            
            self.next_obj.prev_obj = obj
            self.next_obj = obj
            obj.next_obj.push_down()
            
            if self.field_group: self.field_group.add(obj)
    
    # Callback setters.
    def returned(self, callback, params):
        self.on_return_callback = callback
        self.on_return_params = params
    
    # Mutators.
    ###################################################################################
    def slice_text(self):
        max_disp_len = self.max_display_length
        self.text = self.stored_string[self.from_pos:self.from_pos + max_disp_len]
        
    def on_text_input(self, text_to_insert):
        if self.allowed_chars and not (text_to_insert in self.allowed_chars): return
        if self.blocked_chars and (text_to_insert in self.blocked_chars): return
        pos = self.cursor_position
        
        new_str = self.stored_string[:pos] + text_to_insert + self.stored_string[pos:]
        
        if self.allowed_values and not (self.stored_string+text_to_insert in \
                                                            self.allowed_values): return
        
        self.stored_string = new_str
        
        mx = self.max_stored_length
        
        self.cursor_position += 1 if (pos<mx or mx==0) else 0
        
    # Event Mutators.
    def on_backspace(self):
        """on_backspace() - Performs backspace action from cursor_position."""
        
        pos = self.cursor_position
        
        if not (pos - 1 < 0):
            self.stored_string = self.stored_string[:pos - 1] + self.stored_string[pos:]
            self.cursor_position -= 1
            
        else: self.back_space_skipped += 1# TODO: Chain this one.
    
    def on_delete(self):
        pos = self.cursor_position
        self.stored_string = (self.stored_string[:pos] + self.stored_string[pos + 1:])
    
    def on_insert(self, text):
        self.on_delete()
        self.on_text_input(text)
    
    def on_left(self):
        pos = self.cursor_position
        if pos - 1 < 0: self.on_left_underflow()
        else: self.cursor_position = pos - 1
    
    def on_right(self):
        pos = self.cursor_position
        if (pos >= len(self.stored_string)): self.on_right_overflow()
        else: self.cursor_position = pos + 1
    
    def on_ctrl_left(self):
        """on_ctrl_left() - Replicates CTRL+LEFT in common editors.
        
        Shifts cursor position.
        
        Uses on_ctrl_left_underflow() when left_crtl cannot be performed, i.e string
        is either empty, or hs only space.."""
        
        # Add space to left and right of dot(.)
        cur_pos = self.cursor_position
        stored_string_cropped = self.stored_string[:cur_pos][::-1]
        
        string_dot_split = stored_string_cropped.split('.')
        string_dot_modified = " . ".join(string_dot_split)
        string_list = string_dot_modified.split()
        
        if (not string_list) or not len(string_list):
            self.on_ctrl_left_underflow()
            return
        
        # TODO: Test occurence of -1 on last_word_index.
        last_word = string_list[0]
        last_word_length = len(last_word)
        last_word_index = stored_string_cropped.find(last_word)
        self.cursor_position -= (last_word_length + last_word_index)
        
    def on_ctrl_right(self):
        """on_ctrl_right() - Replicates CTRL+RIGHT in common editors.
        
        Shifts cursor position.
        
        Uses on_ctrl_right_overflow() when left_crtl cannot be performed, i.e string
        is either empty, or hs only space.."""
        
        cur_pos = self.cursor_position
        stored_string_cropped = self.stored_string[cur_pos:]
        
         # Add space to left and right of dot(.)
        string_dot_split = stored_string_cropped.split('.')
        string_dot_modified = " . ".join(string_dot_split)
        string_list = string_dot_modified.split()
        
        if (not string_list) or not len(string_list):
            self.on_ctrl_right_overflow()
            return
        
        # TODO: Test occurence of -1 on last_word_index.
        first_word = string_list[0]
        first_word_length = len(first_word)
        first_word_index = stored_string_cropped.find(first_word)
        self.cursor_position += (first_word_length + first_word_index)
    
    def on_key_down(self, key, mod):
        mods_int = mod#pygame.key.get_mods()
        
        capslock = mods_int & pygame.KMOD_CAPS
        ctrl = mods_int & pygame.KMOD_CTRL
        shift = mods_int & pygame.KMOD_SHIFT
        
        if len(key) == 1:
            if capslock and shift: key = key.lower()
            elif capslock or shift: key = key.upper()
            else: key = key.lower()
            
            if shift: key = self.convert_key(key)
            
            self.on_text_input(key)
            return
        elif len(key) == 3:
            if shift: key = self.convert_key(key)
            
            self.on_text_input(key[1])
            
        if key == "space":
            self.on_text_input(" ")
            return 
            
        if key == "backspace":
            self.on_backspace()
            return
            
        if key == "delete":
            self.on_delete()
            return
            
        if not ctrl: 
            if key in ("left", "left ctrl"):
                self.on_left()
                return
                
            if key in ("right", "right ctrl"):
                self.on_right()
                return
                
        else:
            if key in ("left", "left ctrl"):
                self.on_ctrl_left()
                return
                
            if key in ("right", "right ctrl"):
                self.on_ctrl_right()
                return
                
        if key in ("return", "enter"): self.on_return()
    
    def on_key_up(self, key):
        pass
        
    def on_key_event(self, event, key):
        
        mods_int = pygame.key.get_mods()
        
        capslock = mods_int & pygame.KMOD_CAPS
        ctrl = mods_int & pygame.KMOD_CTRL
        shift = mods_int & pygame.KMOD_SHIFT
        
        if event.type == pygame.KEYDOWN:
            self.on_key_down(key, event.mod)
            
        if event.type == pygame.KEYUP:
            self.on_key_up(key)
        
    # Use if previous and next text_lines are availbale
    # Chain methods/Overflow or Underflow types.
    def on_ctrl_left_underflow(self):
        """on_ctrl_left_underflow() - Performs on_left_crtl on previous object.
        if availbale.
        
        Executes the chain."""
        
        if self.prev_obj: self.prev_obj.on_ctrl_left()
    
    def on_ctrl_right_overflow(self):
    
        if self.next_obj: self.next_obj.on_ctrl_right()
    
    def on_left_underflow(self):
        if self.prev_obj: 
            self.on_focus_lost()
            self.prev_obj.gain_focus()
            
    def on_right_overflow(self):
        if self.next_obj: 
            self.on_focus_lost()
            self.prev_obj.gain_focus()
            
    def convert_key(self, key):

        shift_dict = {
            "[" : "{",
            "]" : "}",
            "`" : "~",
            ";" : ":",
            "'" : "\"",
            "\\" : "|",
            "," : "<",
            "." : ">",
            "/" : "?",
            
            '=' : '+',
            '-' : '_',
            
            "1" : "!",
            "2" : "@",
            "3" : "#",
            "4" : "$",
            "5" : "%",
            "6" : "^",
            "7" : "&",
            "8" : "*",
            "9" : "(",
            "0" : ")",
        }
        
        # If char shift is required, return the changed char.
        if shift_dict.has_key(key): return shift_dict[key]
            
        else: return key
    
    def on_focus_gained(self):
        """on_focus_gained() sets focus to this object.
        
        Executes the lose focus chain to lose all other focused objects."""
        
        self.keyboard_focus = True
        self.cursor_visible = True
        
        # Lose focus chain.
        prev = self.prev_obj
        next = self.next_obj
        while prev:
            prev.on_focus_lost()
            prev = prev.prev_obj
            
        while next:
            next.on_focus_lost()
            next = next.next_obj
        
    def on_focus_lost(self):
        self.keyboard_focus = False
        self.cursor_visible = False
        
    def add_to_next(self, obj):
        if not self.next_obj: self.next_obj = obj
        else: self.next_obj.add_to_next(obj)
        
    def gain_focus(self):
        self.keyboard_focus = True
    
    def update(self):
        pass
    def draw(self, surface):
        AbstractTextLine.draw(self, surface)
        
        
        ####################################################################
        # Updates the visibility of the cursor.
        self.current_time = time.time()
        self.time_diff = self.current_time - self.previous_time
        self.previous_time = self.current_time
        
        self.cursor_ms_counter += self.time_diff * 1000
        cur_pos = self.cursor_position
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible
            
        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.stored_string[:cur_pos])[0]
            
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if cur_pos > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            if self.keyboard_focus:
                self.draw_cursor(surface)
        
    def draw_cursor(self, surface):
        if not self.cursor_visible: return
        height = self.get_size("a")[1]
        
        cur_pos = self.cursor_position
        
        if cur_pos - self.from_pos : x_var = \
                        self.get_size(self.stored_string[self.from_pos:cur_pos])[0] - 1
        else: x_var = 0
        
        x, y =  self.text_rect.x, self.text_rect.y
        pygame.draw.line(surface, (self.text_color), (x + x_var, y), (x+x_var,y+height))

## Simplified LMR and faster
#class LMRNumberTextLine(LMRTextLine):
#    def __init__(self, initial_string = ""):
#        LMRTextLine.__init__(initial_string)
#        
        
class TextFieldSingleLine(LMRTextLine, Button):
    g_Mouse = None
    def __init__(self, panel = None, initial_string = "", size=None):

        LMRTextLine.__init__(self, initial_string = initial_string)
        
        # TODO: seperate Button and amke a universal abstract handler for events.
        Button.__init__(self, panel)
        
        self.label = "T123"
        
        # Self properties.
        self.background_color = (250, 250, 250)
        
        # Other class setters.
        self.text_color = (76, 76, 76)
        self.font_size = 20
        self.font_family = "Serif"
        
        self.alignment = -1
        
        if size:
            surf = pygame.Surface(size)
        else:
            surf = pygame.Surface((self.get_size("0000")[0]+20, 20))
            
        surf.fill(self.background_color)
        
        self.theme = create_button_theme(surf.copy(), surf.copy(), surf.copy())
        self.default = surf.copy()
        self.rect = surf.get_rect()
        
        self.keyboard_focus = False
        
        self.padding = (6, 6) # left right padding.
        
        self.clicked(self.on_focus_gained, ())
        
        self.ready = True
        self.adjust_text_rect()
        self.blit_text()
        
    @staticmethod
    def create_mouse_object():
        TextFieldSingleLine.g_Mouse = Mouse()
    
    # Setter.
    def set_name(self, name):
        self.name = name
    
    def align(self, alignment): #(-1, 0, 1) = (left, center, right).
        self.alignment = alignment
        
    # Getter.
    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.stored_string # CHANGED HERE.
        
    def adjust_text_rect(self):
        text_rect, text_cropped_rect = TextFieldSingleLine.get_text_rects(self)
        
        rect = self.rect
        pl, pr = self.padding
#       
        cy = self.rect.height/2
        
        if self.alignment == -1:
            x = pl
            
        text_rect.x, text_rect.centery = x, cy
        
        text_cropped_rect.width = self.rect.width - (pr + pr)
    
    def string_changed(self):
        self.blit_text()
        
    def assign_field(self, obj):
        self.field_group = obj
        LMRTextLine.returned(self, self.field_group.on_return, ())
    
    def blit_text(self):
        self.theme["default"].fill(self.background_color)
        self.theme["hover"].fill(self.background_color)
        self.theme["pressed"].fill(self.background_color)
        
        self.theme["default"].blit(self.default_theme["default"], (0, 0))
        self.theme["hover"].blit(self.default_theme["default"], (0, 0))
        self.theme["pressed"].blit(self.default_theme["default"], (0, 0))
        
        # Draws cursor automatically if required.
        LMRTextLine.draw(self, self.theme["default"])
        LMRTextLine.draw(self, self.theme["hover"])
        LMRTextLine.draw(self, self.theme["pressed"])
    
    def alter_focus(self):
        self.keyboard_focus = not self.keyboard_focus
        
    def on_focus_lost(self):
        if not self.keyboard_focus: return
        
        LMRTextLine.on_focus_lost(self)
        
        
        self.adjust_text_rect()
        self.blit_text()
    
    def on_focus_gained(self):    
        
        LMRTextLine.on_focus_gained(self)
        
        if self.field_group: self.field_group.gain_keyboard_focus(self)
        
        if self.g_Mouse:
            self.g_Mouse.update()
            x, y = self.g_Mouse.get_pos()
            x = x - self.rect.x
    
    def on_key_down(self, key, mod):
        
        LMRTextLine.on_key_down(self, key, mod)
        
        self.adjust_text_rect()
        
        self.blit_text()
        
    def on_key_event(self, event, key):
        
        if (not self.keyboard_focus): return
        
        LMRTextLine.on_key_event(self, event, key)
        
    def draw(self, surface):
        """Draws the final Textbox to the screen."""
        
        self.blit_text()
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        pass
    
class TextField(pygame.sprite.Group):
    def __init__(self):
        
        pygame.sprite.Group.__init__(self)
        TextFieldSingleLine.create_mouse_object()
        self.on_return_callback = self.null
        self.on_return_params = ()
        
    def null(self,):
        pass
        
    def draw(self, surface):
        
        sprites = self.sprites()
        
        for spr in sprites:  
            spr.draw(surface)
        
        self.lostsprites = []
        
    def add(self, *params):
        pygame.sprite.Group.add(self, *params)
        
        for spr in params:
            spr.assign_field(self)
        
    def gain_keyboard_focus(self, spr_obj):# Callback to clicked of TextFieldSingleLine.
        """gain_keyboard_focus() - called when any one of the sprite gains keyfocus."""
        
        sprites = self.sprites()
        
        for spr in sprites:  
            if not (spr == spr_obj): spr.on_focus_lost()
        
        self.lostsprites = []
        
    def update(self):
        sprites = self.sprites()
        
        for spr in sprites:  
            spr.update()
    
    def get_values(self):
        
        dict_ = dict()
        sprites = self.sprites()
        
        for spr in sprites:  
            dict_[spr.get_name()] = spr.get_value()
            
        return dict_
        
    def on_return(self):
        
        self.on_return_callback(*self.on_return_params)
        
    def returned(self, callback, params):
        self.on_return_callback = callback
        self.on_return_params = params
    
    def disable(self):
        pass        
        
