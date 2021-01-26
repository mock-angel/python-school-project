# PipeMethods.py
import pygame
from pygame.locals import *
ORANGE = (155, 63, 10)
GREEN = (75, 116, 110)
GREY = (58, 65, 73)
class Pipe():
    def __init__(self, link):
        self.cell_1 = link[0]
        self.cell_2 = link[1]
        self.pair = link
        self.coord_1 = self.convert_to_points(self.cell_1)
        self.coord_2 = self.convert_to_points(self.cell_2)
        self.color = GREY
        
    def draw(self, Surface):
        pygame.draw.line(Surface, self.color, self.coord_1, self.coord_2, 4)
        if self.color == GREEN: print "green drawn"
    def convert_to_points(self, tuple_):
        x = tuple_[1]*60 + 30 if tuple_[0]%2==0 else tuple_[1]*60 + 60
        y = tuple_[0]*42 + 30
        return (x, y)
        
    def change_color(self, color):
        self.color = color
    
class PipeMethods():
    def __init__(self):
        self.pipe_group = set([])
        
    ########################################################################
    # Pair, link management.
    def get_all_orange_cells(self):
        nodes = self.nodes()
        for node in nodes:
            # If its either a system core or just none or utilities
            if node.auth == "None": yield node.cell
                
    def get_all_green_cells(self):
        nodes = self.nodes()
        for node in nodes:
            if not (node.auth == "root"): continue
                
            if node.n_state == "covered" or not node.is_uncovered_defensive():
                yield node.cell
        
    def get_all_grey_cells(self):
        nodes = self.nodes()
        for node in nodes:
            # If its either a system core or just none or utilities
            if node.auth == "local": yield node.cell
                
            elif node.is_uncovered_defensive(): yield node.cell
                
    def create_orange_connection_pairs(self, orange_cells_set):
        """Make orange cells have orange links with orange_cells."""
        
        pairs = set([])
        for orange_cell in orange_cells_set:
            neighbours = self.get_neighbouring_node_cells(orange_cell)
            
            pairable_neighbours_li = set(orange_cells_set) & neighbours
            for cell in pairable_neighbours_li:
                if (cell, orange_cell) not in pairs:
                    pairs.add((orange_cell, cell))
        
        return pairs
        
    def create_green_connection_pairs(self, orange_cells_set, green_cells_set):
        """Make green_cells have green links with orange cells."""
        
        pairs = set([])
        
        for green_cell in green_cells_set:
        
            neighbours = self.get_neighbouring_node_cells(green_cell)
            pairable_neighbours_li = orange_cells_set & neighbours
            for cell in pairable_neighbours_li:
                if (cell, green_cell) not in pairs:
                    pairs.add((green_cell, cell))
        return pairs
        
    def create_grey_connection_pairs(self, orange_cells_set, green_cells_set, grey_cells_set):
        """Make grey cells have grey links wih grey and green cells."""
        
        pairs = set([])
        
        green_and_grey_cells_set = (green_cells_set|grey_cells_set)
        
        for grey_cell in green_and_grey_cells_set:
        
            neighbours = self.get_neighbouring_node_cells(grey_cell)
            pairable_neighbours_li = (green_and_grey_cells_set)&neighbours
            
            if grey_cell in grey_cells_set: pairable_neighbours_li |= orange_cells_set
            
            for cell in pairable_neighbours_li:
                if (cell, grey_cell) not in pairs: pairs.add((grey_cell, cell))
        return pairs
    ########################################################################
    # NodeLink sprite init.   
    def create_all_connection_pairs(self, all_cells_set):
    
        pairs = set([])
        for cell in all_cells_set:
        
            neighbours = self.get_neighbouring_node_cells(cell)
            pairable_neighbours_li = all_cells_set & neighbours
            for p_cell in pairable_neighbours_li:
                if (p_cell, cell) not in pairs:
                    pairs.add((cell, p_cell))
        return pairs
        
    def generate_pairs(self):
        node_cells = set(self.get_node_cells())
        node_pairs = self.create_all_connection_pairs(node_cells)
        for pair in node_pairs: self.pipe_group.add(Pipe(pair))
    
    ########################################################################
    def pipes(self):
        return self.pipe_group
    
    def draw(self, surface):
        pipes = self.pipes()
        for pipe in pipes: pipe.draw(surface)

    def update_links(self):
        
        orange_cells_set = set(self.get_all_orange_cells())
        green_cells_set = set(self.get_all_green_cells())
        grey_cells_set = set(self.get_all_grey_cells())

        orange_pairs = self.create_orange_connection_pairs(orange_cells_set)
        green_pairs = self.create_green_connection_pairs(orange_cells_set, green_cells_set)
        grey_pairs = self.create_grey_connection_pairs(orange_cells_set, green_cells_set, grey_cells_set)
        
        for pipe in self.pipes():
            pair = pipe.pair

            if pair in grey_pairs or pair[::-1] in grey_pairs:
                pipe.change_color(GREY)
                
            elif pair in orange_pairs or pair[::-1] in orange_pairs:
                pipe.change_color(ORANGE)
                
            elif pair in green_pairs or pair[::-1] in green_pairs:
                pipe.change_color(GREEN)
