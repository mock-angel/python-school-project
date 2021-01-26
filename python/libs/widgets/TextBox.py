# TextBox.py
import pygame
from Text import TextLine

class AutoScrollingTextBox:
    """AutoScrollingTextBox
    
    Some properties:
        line_height - height of every line.
        max_lines -  calculated automatically."""
        
    def __init__(self, rect, font_name = None, size = 10):
        self.text = TextLine(text="se", font=font_name, size=size)
        
        self.rect = rect
        
        self.font_name = font_name
        self.size = size
        (width, height) =self.text.get_size("A")
        self.line_height = height
        self.max_lines = self.rect.height/self.line_height - 1
        
        # List of lines starts out empty.
        self.lines = []
        
    def add_line_internal(self, new_line):
        
        # New object being created for the new_line that is posted.
        text = TextLine(text=new_line, font=self.font_name, size=self.size)
        text.rect.centerx = self.rect.x + self.rect.width/2
        
        # If the line count exceeds the limit, move all lines one step up.
        if len(self.lines) >= self.max_lines:
            
            # Move all lines one step up.
            for txt_obj in self.lines:
                txt_obj.rect = txt_obj.rect.move(0, -self.line_height)
                
            text.rect.center = txt_obj.rect.center
            text.rect = text.rect.move(0, self.line_height)
        
        # If there are no lines.
        elif not len(self.lines):
            text.rect.centery = self.rect.y + self.line_height/2
            text.rect.centerx = self.rect.x + self.rect.width/2
        
        # If there are a few lines, and it doesn't exceed the max_lines limit.
        else: 
            text.rect.center = self.lines[-1].rect.center
            text.rect = text.rect.move(0, self.line_height)
            
        self.lines.append(text)
        
    def post(self, message):
        """post() - Creates a new line of text and appends it at the end."""
        width, height = self.text.get_size(message)
        
        excess = ""
        
        # If the line cannot fit in the box, create a new line for the excess chars.
        if width > self.rect.width:
            
            while width > self.rect.width:
                excess = message[-1] + excess
                message = message[0:-1]
                
                (width, height) = self.text.get_size(message)
        
        # If there is any excess chars.
        if len(excess) > 0:
            if message[-1].isalnum() and excess[0].isalnum():
                excess = message[-1] + excess
                message = message[0:-1] + '-'
                
                message = message[0:-1] if message[-2] == ' ' else message#remove the'-'
        
        self.add_line_internal(message)
        
        # Uses recursion to post excess chars.
        excess = excess.strip() # Remove white spaces before and after text.
        if len(excess) > 0: self.post(excess)
    
    def clear(self):
        del self.lines[:]
    
    def draw(self, surface):
        
        # Calculate start pos of drawing the text.
        diff = len(self.lines) - self.max_lines
        start_pos = diff if diff > 0 else 0 
        
        # Draw the rectangle.
        color = (11, 11, 11)
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw lines now.
        line_li = self.lines[start_pos:]
        for text in line_li:
            text.draw(surface)
            
