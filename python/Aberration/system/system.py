#from node import Node
#from NodeCluster import NodeCluster
from locals import tooltip_dict
from locals import *
# TODO: import and create ToolTip
import pygame
from pygame.locals import *
from widgets import ToolTip
from NodeCluster import NodeCluster
class System(pygame.sprite.Sprite):
    __sys = None
    @staticmethod
    def get_system():
        return System.__sys
        
    def __init__(self):
        super(System, self).__init__()
        if not System.__sys: System.__sys = self
        else: return
        self.ready = False
        self.init_surfaces()
        self.cluster = NodeCluster()
        self.cluster.generate_node()
        self.cluster.connect(self)
        #self.all_nodes = self.cluster.nodes()
        #self.defensive_subsystem_nodes = pygame.sprite.Group()
        
        self.init_tooltip()
        
        self.require_update = True
        self.ready = True
        self.refresh()
            
    def init_surfaces(self):
        """Initialise default surfaces."""
        self.default = pygame.Surface((pygame.display.get_surface().get_rect().width, pygame.display.get_surface().get_rect().height)).convert_alpha()
        self.default.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        
        self.image = self.default.copy()
        
    def init_tooltip(self):
        """Initialise tooltip surface images."""
        
#        self.tip.add_tip(key, tip_img.anti_virus)
#        self.tip.add_tip(key, surface_value)
        
        #TODO: add keys and also define the ToolTip class.
        self.hover_message = ToolTip()
        self.hover_message.add_tipdict(tooltip_dict)
        self.cluster.feed(self.hover_message)
        self.hover_message.change_tip(WET)
        size = pygame.display.get_surface().get_size()
        
        h_size = self.hover_message.image.get_size()
        
        cx = (size[0] - h_size[0]/2)
        cy = (size[1] - h_size[1]/2)
        
        self.hover_message.rect.center = cx, cy
        #self.hover_message.rect.width = pygame.display.get_surface().get_rect().height
        #dirr = "data/themes/default/message/"
        
    ####################################################################
    # Setters.
    def infect(self, virus):#include_virus
        """Assign the virus object."""
        self.virus = virus
    
    def defend(self, node):#defend virus
        """__.__"""
#        self.virus.coherence -= node.strength
#        node.coherence -= self.virus.strength
        print node.coherence, "node coh", self.virus.strength
    ####################################################################
    # Getter.
    
    ####################################################################
    # Mutator.
    def update(self):
        """updates all the links."""
        pass
        #self.virus.mouse.update()# TODO: change to virus.update().
        
    def update_list(self):
        pass
        
    def refresh(self):# draw_everything
        """Refreshes the system screen with the latest known data."""
        
        draw_surface = self.default.copy()
        
        # Draw all the node links and then the sprites.  Drawing of the
        # tooltip comes next.
        
        self.cluster.draw(draw_surface)
        self.hover_message.draw(draw_surface)# TODO
        
        # Image is set to draw_surface.
        self.image = draw_surface#.copy()
        print "System refreshed."
    
    # Game Operations.
    def update_links(self):
        self.cluster.update_links()
    
    def next_turn(self, io_node):
        self.virus.next_turn(io_node)
        
    ####################################################################
    # Callbacks.
    def node_clicked_callback(self, io_node):#check
        """Called by the node.on_clicked() method as a callback to this
        method when the node is clicked.
        
        Callback from the Node object is called when a node is
        clicked.  First perform touch on node, then update links.
        
        A final update is called and the nthe system screen is refreshed.
        """
        print "*" * 75
        detect_changed =  io_node.touch()
        
        self.update_links()
        print "link updated"
        if detect_changed: self.next_turn(io_node)
            
        self.update()
        self.node_enter_callback(io_node)
        
    def node_enter_callback(self, io_node): # check.
        """The virus's cursor is hovering this node."""
        
        self.hover_message.change_tip( io_node.get_property())
        self.refresh()
        
    def node_left_callback(self, io_node): # check.
        """The virus's cursor left the node."""
        
        self.hover_message.change_tip(None)
        self.refresh()
        
    def set_abberation(self, obj):
        self.abberation = obj
        
    def lost(self):# If virus lost.
        self.abberation.switch_screen(2) # END_GAMESCREEN.
    ####################################################################
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
