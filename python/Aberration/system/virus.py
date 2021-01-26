# virus.py
"""
Slot(int)
    io_node - The node selected the current turn, its None during game beginnning.
virus()
    The main virus class.
"""
from locals import SELF_REPAIR, KERNEL_ROT, POLYMORPHIC_SHIELD, SECONDARY_VECTOR
from widgets.Button import Button, ButtonGroup, create_button_theme
from widgets.Text import TextWall, TextLine
from widgets.Panel import Panel
import system
#import system
import pygame

COHERENCE_COLOR = (150, 63, 10)
STRENGTH_COLOR = (151, 26, 26)

def combine_image(main_surf, sub_surf):
        """Blit Symbol of utility subsystem to slot"""
        using_surf = main_surf.copy()
        using_surf.blit(sub_surf, (0,0))
        return using_surf
        
class Slot(Button):
    
    directory = "data/themes/default/slot/"
    
    slot_default =  pygame.image.load(directory + "slot.png")
    slot_hover = pygame.image.load(directory + "slot_hover.png")
    
    symbols_dict = {
        "Self_repair" : pygame.image.load(directory + "Self_repair.png"),
        "Secondary_vector" : pygame.image.load(directory + "Secondary_vector.png"),
        "Polymorphic_shield" : pygame.image.load(directory + "Polymorphic_shield.png"),
        "Kernel_rot" : pygame.image.load(directory + "Kernel_rot.png"),
    
    }
    
    NULL = {
        "theme" : create_button_theme(slot_default, slot_hover),
        "effect" : (3, 10),# use choice later.
        "turns" : 3,
    }
    
    d = combine_image(slot_default, symbols_dict["Self_repair"])
    h = combine_image(slot_hover, symbols_dict["Self_repair"])
    c_self_repair = {
        "theme" : create_button_theme(d, hover = h),
        "effect" : 3,# use choice later.
        "turns" : 3,
    }
    
    d = combine_image(slot_default, symbols_dict["Secondary_vector"])
    h = combine_image(slot_hover, symbols_dict["Secondary_vector"])
    c_secondary_vector = {
        "theme" : create_button_theme(d, hover = h),
        "effect" : (3, 10),# use choice later.
        "turns" : 3,
    }
    
    d = combine_image(slot_default, symbols_dict["Polymorphic_shield"])
    h = combine_image(slot_hover, symbols_dict["Polymorphic_shield"])
    c_polymorphic_shield = {
        "theme" : create_button_theme(d, hover = h),
        "effect" : (3, 10),# use choice later.
        "turns" : 3,
    }
    
    d = combine_image(slot_default, symbols_dict["Kernel_rot"])
    h = combine_image(slot_hover, symbols_dict["Kernel_rot"])
    c_kernel_rot = {
        "theme" : create_button_theme(d, hover = h),
        "effect" : (3, 10),# use choice later.
        "turns" : 3,
    }
    
    
    nodec_to_slotc_dict = {
        SELF_REPAIR : c_self_repair,
        KERNEL_ROT : c_kernel_rot,
        POLYMORPHIC_SHIELD : c_polymorphic_shield,
        SECONDARY_VECTOR : c_secondary_vector,
    }
    
    # Cleanup.
    d = h = symbols_dict = slot_default = slot_hover = None
    del d, h, symbols_dict, directory, slot_default, slot_hover
    
    
    NULL
    c_self_repair, c_secondary_vector
    c_polymorphic_shield, c_kernel_rot
    nodec_to_slotc_dict
    
    @staticmethod
    def convert_container(nodecontainer):
        """Convert Node.container to Slot.container type."""
        return Slot.nodec_to_slotc_dict[nodecontainer]
    
    @property
    def container(self):
        return self.container_
    @container.setter
    def container(self, container):
        self.container_ = container
        
        self.theme = self.container_["theme"].copy()
        
        # Make a copy of the theme.
        self.theme_current_dup = dict()
        
        theme = self.theme
        for key in theme:
            self.theme_current_dup[key] = theme[key].copy()
        
        # extract the turns and effect.
        self.turns = self.container_["turns"]
        self.effect = self.container_["effect"]
        
        
        
    def __init__(self, container, i):
        super(Slot, self).__init__(Panel.get_first())
        
        self.ready = False
        
        self.index = i
        
        self.active = False
        self.turns = 0
        self.occupied = False
        
        self.container_ = Slot.NULL
        self.theme = self.container_["theme"]
        self.container = container
        
        self.io_node = None
        self.require_update = True
        
        self.clicked(self.activate, ())
        self.text_surf = TextLine()
        
        self.ready = True
        
    def self_repair(self):
        self.io_node.System.virus.coherence += self.effect
        
#    def secondary_vector(self):
#    def polymorphic_shield(self):
#    def kernel_rot(self):
    
    # Getters.
    def is_occupied(self):
        return self.occupied
    
    def draw_values(self):
        
        
        # Make a copy of the theme.
        theme_d = dict()
        theme_dup = self.theme_current_dup
        for key in theme_dup:
            theme_d[key] = theme_dup[key].copy()
        
        
        for key in theme_d:
            surf = theme_d[key]

            #TODO: Will this work?:
            #   fill, then make transparant, blit default image then this image.
            
            self.text_surf.text = str(self.turns)
            surf.blit(self.text_surf.image, (29, 46))
#            
            print "blitting values...."
        self.theme = theme_d
        
    def next_turn(self, io_node):
        """Should be called everytime user clicked a node."""
        
        if io_node: self.io_node = io_node
        
        if not self.active: return False
        
        if self.turns > 0:
            self.turns -= 1
            
            # Run the associated method.
            if self.container == Slot.c_self_repair:
                self.self_repair()
                print "self.self_repair()"
            elif self.container == Slot.c_secondary_vector:
                self.secondary_vector()
                
            elif self.container == Slot.c_polymorphic_shield:
                self.polymorphic_shield()
                
            elif self.container == Slot.c_kernel_rot:
                self.kernel_rot()
            
            # If it runs out of turns.
            if self.turns == 0:
                self.empty()
        if self.active:
            # draw values everyturn.
            self.draw_values()
            
    def empty(self):
        """"Empty the slot so it can hold some other container.
        
        This is done by resetting all variables to its starting values.
        """
        
        self.active = False
        self.turns = 0
        self.occupied = False
        
        self.container = Slot.NULL
        
    def activate(self):
        """Activate the slot holding the subsystem."""
        if not self.active and self.occupied:
            self.active = True
            system.System.get_system().next_turn(None)
        
    def hold(self, container):
        """ """
        if not self.is_occupied():
            self.container = container
            self.occupied = True
            self.active = False

class SlotsHolder(ButtonGroup):
    def __init__(self, amount = 3):
        super(SlotsHolder, self).__init__()
        
        self.length = amount
        self.slot_dict = {} 
        span_width = 168
        bottom = 2
        
        max_w = pygame.display.get_surface().get_rect().width
        max_h = pygame.display.get_surface().get_rect().height
        
        slot_w = Slot.NULL["theme"]["default"].get_rect().width
        start_x = (max_w - span_width + slot_w)/2
        
        padding = (span_width - amount*slot_w)/2
        cy = max_h - ((slot_w/2) + bottom)
        
        for i in range(amount):
            
            # TODO: create a center x,y.
            
            self.slot_dict[i] = Slot(Slot.NULL, i)
            cx = start_x + (padding + slot_w)*i
            self.slot_dict[i].rect.center = cx, cy
            
            self.add(self.slot_dict[i])
            # FIXME: rect reposition please.
    def fill(self, nodecontainer):
        slots = self.slots()
        
        for slot in slots:
            c_container = Slot.convert_container(nodecontainer).copy()

            if not slot.is_occupied():
                slot.hold(c_container)
                return True
        return False
    def slots(self):
    
        slot_list = []
        
        slots = self.slot_dict
        for key in slots:
            slot_list.append(self.slot_dict[key])
            
        return slot_list
    def next_turn(self, io_node):
        """Needs to be called everytime node is pressed."""
        for slot in self.slots():
            slot.next_turn(io_node)
    
class Virus(pygame.sprite.Sprite):

    coherence_ = 0
    strength_ = 0
    
    def __init__(self):
        super(Virus, self).__init__()
        self.ready = False
        
        self.init()
        self.slots_holder = SlotsHolder(3)
        
        #TODO: *Difficulty [virus, system, locals]
        self.coherence = 70
        self.strength = 25
        print "Virus initialised."
        
        self.ready = True
    
    def infect(self, system):
        self.System = system
        self.System.virus = self
    def init(self):
        
        self.transp_screen = pygame.Surface((pygame.display.get_surface().get_rect().width, pygame.display.get_surface().get_rect().height)).convert_alpha()
        self.transp_screen.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        
        self.rect = self.transp_screen.get_rect()
        
        self.text_surf = TextLine(size = 15)
        
        # -- left panel.
        # Background layer
        self.l_background_surf = pygame.Surface((132, 132))
        self.l_background_surf.fill((3, 3, 3))
        
#        # Make the alpha image.
        self.l_foreground_surf = pygame.image.load("data/themes/default/NODE/Virus_stats.png").convert_alpha()
        
        # Draw the foreground over the background.
        l_surf = self.l_background_surf.copy()
        l_surf.blit(self.l_foreground_surf, (0, 0))
        
        #self.refresh()
        # left screen
        self.l_rect = l_surf.get_rect()
        self.l_rect.x += 20
        self.l_rect.bottom = (pygame.display.get_surface().get_rect().height - 20)
        
        # centerslots
#        Slots
#        self.slot_dict = {
#            0: Slot(0),
#            1: Slot(1),
#            2: Slot(2),
#        }
        
        # Original virus screeen.
        active_surf = self.transp_screen.copy()
        active_surf.blit(l_surf, (self.l_rect.x, self.l_rect.y))
        
        self.image = active_surf.copy()
        
    #################################################################
    # Setters.
    @property
    def coherence(self):
        return self.coherence_
        
    @property
    def strength(self):
        return self.strength_
    #################################################################
    # Getters.
    @coherence.setter
    def coherence(self, value):
        self.coherence_ = value
        
        print "virus coherence changed ", self.coherence_, ": refreshing Virus."
        self.refresh()
        
    @strength.setter
    def strength(self, value):
        self.strength_ = value
        
        print "virus strength changed ", self.coherence_, ": refreshing Virus."
        self.refresh()
        
    #################################################################
    # Mutator.
    def refresh(self):
        """Used to refresh the sprite image when either coherence or
        strength changes.
        """  
        # TODO: needs a lot of improvement.
        active_surface = self.l_background_surf.copy()
        
        coh_height = 72 * (self.coherence/ 100.)
        stre_height = 72 * (self.strength/ 100.)
        
        coherence_rect = [9, 33+72-coh_height, 24, coh_height]
        strength_rect = [132 - 8-24, 33+72-stre_height, 24, stre_height]
        
        pygame.draw.rect(active_surface, COHERENCE_COLOR, coherence_rect)
        pygame.draw.rect(active_surface, STRENGTH_COLOR, strength_rect)
        
        active_surface.blit(self.l_foreground_surf, (0, 0))
        
        self.text_surf.text = str(self.coherence)
        active_surface.blit(self.text_surf.image, (65, 26))
        
        self.text_surf.text = str(self.strength)
        active_surface.blit(self.text_surf.image, (67, 100))
        
        self.l_rect = active_surface.get_rect()
        self.l_rect.x += 20
        self.l_rect.bottom = (pygame.display.get_surface().get_rect().height - 20)
        
        # Original virus screeen.
        active_surf = self.transp_screen.copy()
        active_surf.blit(active_surface, (self.l_rect.x, self.l_rect.y))
        
        self.image = active_surf
        
        print "Virus refreshed"
        
    def draw(self, surface):
        
        surface.blit(self.image, (0, 0))
        self.slots_holder.draw(surface)
        
    # -- Used by node callback method of class System during node.clicked() .
    def next_turn(self, io_node):# TODO: complete this
        """Active subsystems require to know everytime user clicks any node"""
        self.slots_holder.next_turn(io_node)
        
        if self.coherence <=0:
            self.System.lost()
        
    def add_utility(self, container):
        
        return self.slots_holder.fill(container)
