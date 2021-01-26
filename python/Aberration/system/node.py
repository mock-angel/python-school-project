# node.py
import pygame
from pygame.locals import *

#Templates
from widgets import Button, ButtonGroup
from widgets import TextLine
from locals import *

def sep_theme(theme):
    
    new_theme = dict()
    for key in theme:
        new_theme[key] = theme[key].copy()
    return new_theme
    
class Node(Button):

    Utility_Subsystem_list = [
        SELF_REPAIR, KERNEL_ROT,
        POLYMORPHIC_SHIELD, SECONDARY_VECTOR
    ]
    
    Defensive_Subsystem_list = [
        FIREWALL, ANTIVIRUS, 
        RESTORER, SUPPRESSOR
    ]
    
    ###################################################################
    # --- Node Sprite initialisation.
    def __init__(self, panel, cell):
        Button.__init__(self, panel)
        self.ready = False
        
        self.require_update = False
        self.cell_t = cell
        
        self.tooltip = None
        
        self.base_theme = dict()
        
        self.init()
        
        self.require_update = True
        self.ready = True
        
    def init(self):
        """init image values?"""
        
        self.neighbours_list = set([])
        
        self.auth = "local"             # local/root.
        self.n_state = "covered"        # covered/uncovered.
        
        self.strength_ = 0
        self.coherence_ = 0
        
        self.System = None # Where the system object goes.

        self.container_ = None # Can take values of the subsystem.
        self.hidden_container = None # Only when sub_system = DATA_CACHE.
        
        self.text_surf = TextLine()
        
        #self.node_template = ENCRYPTED
        
        self.update_theme()
        
    ###################################################################
    # Mutator.
    def update_theme(self):
        """Updates button theme based on the container.
        
        Called everytime the node state or container is updated."""
        
        if self.auth=="local":
                self.n_theme = DRY if self.state_ == "covered" else DRY
                
        elif self.auth=="root":
            self.n_theme = WET if self.state_ == "covered" else self.container
            
        elif self.auth == "None":
            
            self.n_theme = HACKED
            
        if not self.tooltip: return
        
    def configure_posiion(self):
        """Sets the node in the specific location on the screen."""
        
        self.rect = self.image.get_rect()
        
        x = self.cell[1] * 60 + 30 if self.cell[0] % 2 == 0 else self.cell[1] * 60 + 60
        y = self.cell[0] * 42 + 30
        self.rect.center = x, y

    def blit_values(self):
        """Takes care of any text that is reqired to be blitted to the node.
        
        Coherence and Strength are blitted if the node is rooted and uncovered."""
        
        
        
        if (self.auth == "root"
            and self.n_state == "uncovered" 
            and self.container in self.Defensive_Subsystem_list + [SYSTEM_CORE]
        ):
            new_theme = sep_theme(self.base_theme)
            
            for key in new_theme:
                self.text_surf.text = str(self.coherence)
                new_theme[key].blit(self.text_surf.image, (29, 4))
                
                self.text_surf.text = str(self.strength)
                new_theme[key].blit(self.text_surf.image, (29, 46))
            
            self.theme = new_theme
    
    def feed(self, tooltip):
        self.tooltip = tooltip
    
    ###################################################################
    # Getters.
    def get_linked_neighbours(self):
        """Get a list of linked nodes in the form of a list."""
        
        return list(self.neighbours_list)
        
    def get_neighbour_cells(self):
        """Get a list of cells of linked node."""
        
        linked_neighbours = self.get_linked_neighbours()
        
        cell_set = set([])
        
        for node in linked_neighbours:
            cell_set.add(node.cell)
        
        return cell_set
    
    def get_property(self):
        
        if self.auth=="local":
            if self.n_state == "covered":
                return DRY
                
            else:
                self.n_theme = DRY
                
        elif self.auth=="root":
                return WET if self.n_state == "covered" else self.container
                
        elif self.auth == "None":
            
            return HACKED
            
    @property
    def n_theme(self):
        return self.theme
    @property
    def cell(self):
        return self.cell_t
    @property
    def coherence(self):
        return self.coherence_
    @property
    def strength(self):
        return self.strength_
    @property
    def container(self):
        return self.container_
    @property
    def n_state(self):
        return self.state_
        
    ###################################################################
    # Setters.
    def add_neighbours(self, *nodes):# Done.
        """Create link to this node."""
        
        for node in nodes:
            self.neighbours_list.add(node)
        
    def link_system(self, system):# Done.
        """Gives the Node access to the System."""
        
        self.System = system
        
    def clear_linked(self):# Done.
        
        self.neighbours_list.clear()
        
    @n_theme.setter
    def n_theme(self, config):
        # TODO: Complete please.
        self.theme = config.theme
        self.base_theme = dict()
        
        self.base_theme = sep_theme(config.theme)
        
        # Perform rect correction operations here.
        self.configure_posiion()
        
        print "catch the criminal!!"
        self.blit_values()
        
    @cell.setter
    def cell(self, cell):
        self.cell_t = cell
        
        self.configure_posiion()
        
    @coherence.setter
    def coherence(self, value):
        self.coherence_ = value
        print "now value is changing right?", value
        self.blit_values()
            
    @strength.setter
    def strength(self, value):
        self.strength_ = value
        
        self.blit_values()
        
    @container.setter
    def container(self, container):
        self.container_ = container

        self.update_theme()
        
    @n_state.setter
    def n_state(self, state):
        self.state_ = state

        self.update_theme()
        
    def set_container(self, container, hidden_container = None):
        self.container = container
        self.hidden_container = hidden_container
        
        config = container if not(container == DATA_CACHE) else hidden_container
        
        self.coherence, self.strength = config.coherence_strength
        
    ###################################################################
    # Node Operations.
    def root(self):
        """Used on node whose closest node has been uncovered.
        
        Node should not be rooted, nor should it contain a def_subsystem 
        around it.  Also invoked when a rooted defensive node terminates
        and node state was uncovered."""
        
        # Test 0. This node should be unrooted/local to root.
        
        if not (self.auth == "local"): return
        
        # Test 1. Neighboouring nodes are checked for defensive properties
        # No node can safely root while having a rooted defensive node closeby.
        print "Attempting root."
        for node in self.neighbours_list:
            if node.is_uncovered_defensive():
                return
        
        # Check for state being uncovered and container being none
        if self.n_state == "uncovered" and self.container == None: self.auth = "None"
        
        # Now its safe to root.
        else: self.auth = "root"
        
        self.update_theme()
        
    def unroot(self):
        """Remove virus access to this node."""
        
        # Test 0: Unrooting is possible only when node is rooted.
        if not (self.auth == "root"): pass
            
        # Should not be uncovered defensive.
        if self.is_uncovered_defensive(): return
            
        self.auth = "local"
        self.update_theme()
        
    def cover(self):
        """Dead code.  But used to cover uncovered nodes if its made to."""
        
        # covering is not possible once uncovered.
        return
        
    def uncover(self):
        """Uncover nodes if it meets specific conditions.
        
        Node should not be rooted, nor should it contain a def_subsystem 
        around it.  If it encounters an Empty container while uncovering,
        auth is shifted to 'None' to prohibit furthur change on the node."""
        print "Trying to uncover."        
        # Test 0 : Uncover only if its rooted.
        
        if not self.auth == "root": return
        print 111
        # Test 1 : No neighbouring nodes must be rooted and defensive.
        if self.container in self.Defensive_Subsystem_list:
             
            for node in self.get_linked_neighbours():
                node.unroot()
        else:
            for node in self.neighbours_list:
                if node.is_uncovered_defensive():
                    print "FAILED"
                    return
                
        self.state_ = "uncovered"
        
        # auth is set to None if the container has notihing.
        if self.container == None: self.auth = "None"
        
        # if container is the system_core or data_cache, or it has nothing
        # just root all other nodes.
        if self.container == None or self.container in [SYSTEM_CORE, DATA_CACHE, None]:
            for node in self.neighbours_list: node.root()

        print "Uncovered:", self.cell
        self.update_theme()

    def override(self):
        if self.state_ == "uncovered" and self.auth == "root":
            self.auth = "None"
            self.container = None
            for node in self.get_linked_neighbours():
                node.root()
    
    ###################################################################
    # Game Operations.
    def utiliy_subsystem_action(self):
        """"""
        # Tell the virus which utility to add. if adding was successful,
        # change container to None.
        if self.System.virus.add_utility(self.container):
            self.auth = "None"
            self.container = None
            
    def defensive_subsystem_action(self):
        """Action when a defensive node is pressed."""
        
        # Compare virus strength and subsystem coherence.
        
        # No resistance by the subsystem.
        if self.System.virus.strength >= self.coherence:
        
            # If node is a System_Core, tell the System that its hacked..
            if self.container == SYSTEM_CORE:
                self.System.hacked = True
            
            # TODO: Add the script to change it to empty node.
            self.override()
            return
        
        else: 
            self.System.virus.coherence -= self.strength
            self.coherence -= self.System.virus.strength
            self.System.defend(self)

        # If its a Restorer Subsystem.
        if self.container == RESTORER:
            
            # TODO: Please write this script.
            #self.restore_node(20)
            pass
        
        # Printing.            
        v = self.System.virus
        
        print self.container, self.coherence, self.strength,
        print "|", "Virus", v.coherence, v.strength
            
    ###################################################################
    # --- Methods used by other Subsystems nodes.
    #######################################################
    # --- Methods that are used by System.??
    ###################################################################
    def touch(self):
        """When a node is clicked.
        """
        print "Touched", self.cell
        print "neighbours:",self.get_neighbour_cells()
        prev_auth = self.auth 
        prev_state = self.n_state 
        p_c = self.container
        p_theme = self.theme_
        
        if self.auth=="local": pass
        
        elif self.auth=="root":
            if self.n_state == "covered":
                # TODO: put local back.
                self.uncover()
                
            else:
                    # Actions for Data Cache.
                    if self.container == DATA_CACHE:
                        self.container = self.hidden_subsystem
                        self.hidden_subsystem = None
                        
                    # Actions for Utiliy Subsystems.
                    elif self.container in self.Utility_Subsystem_list:
                        self.utiliy_subsystem_action()
                        
                    # Actions for Defensive Subsystem.
                    elif self.container in (self.Defensive_Subsystem_list + [SYSTEM_CORE]):
                        self.defensive_subsystem_action()
                    
        elif self.auth == "None": pass
        print self.n_state, self.container, self.auth
        self.update_theme()
        
        return False if (prev_auth==self.auth and prev_state==self.n_state 
                            and p_c==self.container and p_theme == self.theme_) else 1
        
    def update(self):
        if not self.is_hacked(): return
        for node in self.get_linked_neighbours(): node.root()
    def is_uncovered_defensive(self):
        d_subli = self.Defensive_Subsystem_list
        return True if self.state_=="uncovered" and self.container in d_subli else False
    
    def is_hacked(self):
        return True if self.auth == "None" else False
