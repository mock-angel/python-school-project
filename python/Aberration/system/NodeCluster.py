# NodeCluster.py
import pygame
from pygame.locals import *
from widgets import ButtonGroup, Panel
from node import Node
from PipeMethods import PipeMethods
from locals import *
import random

class CellFactory(object):# old NodeLinkStructureGenerator.
    def __init__(self):
        self.all_cells = [] #cell_tuple_list
        # Stores every cell that is needed to be blank.
        self.all_cells = set()
        self.sink_cells = set()
        self.void_cells = set()#sink_cells_neighbours
        self.free_cells = set()
        self.node_cells = set()
        self.root_cell = (0, 0)
    ###################################################################
    # Setter.
    def assign_diamension(self, max_rc): # TODO: Change to assign size?
        self.max_r, self.max_c = max_rc
    ###################################################################
    # Getters.
    def get_sink_cells(self):
        return list(self.sink_cells)
        
    def get_void_cells(self):
        return list(self.void_cells)
        
    def get_free_cells(self):
        return list(self.free_cells)
        
    def get_all_cells(self):
        return list(self.all_cells)
        
    def get_node_cells(self):
        return list(self.node_cells)
    ########################################################
    # --Neighbour Calculation.
    def get_neighbouring_cells_in(self, cell, set_):
        """Get a set of all the neighbouring cells not in set."""
        # Calculate raw neighbours.
        r, c = cell
        
        surr_cells = set([])
        surr_cells.add((r, c+1))
        surr_cells.add((r, c-1))
        surr_cells.add((r+1, c))
        surr_cells.add((r-1, c))
        
        if (r % 2 == 0):
            surr_cells.add((r+1, c-1))
            surr_cells.add((r-1, c-1))
        else:
            surr_cells.add((r+1, c+1))
            surr_cells.add((r-1, c+1))
        
        # Eleminate neighbours that can never exist.
        invalid_surr_cells = set()
        
        for (cell_rc) in surr_cells:
            cell_r, cell_c = cell_rc
            
            # Cells should be present in set.
            if cell_rc not in set_:
                invalid_surr_cells.add(cell_rc)

        # Deletion.
        surr_cells -= invalid_surr_cells
        
        # Finally throw the result.
        return surr_cells
    
    def get_all_neighbouring_cells(self, cell):
        """Get a set of all the surrounding cells."""
        return self.get_neighbouring_cells_in(cell, self.all_cells)
        
    def get_neighbouring_free_cells(self, cell):
        """Get a set of all the neighbouring free cells."""
        return self.get_neighbouring_cells_in(cell, self.free_cells)
    
    def get_neighbouring_void_cells(self, cell):
        """Get a set of all the neighbouring void cells."""
        return self.get_neighbouring_cells_in(cell, self.void_cells)
    
    def get_neighbouring_node_cells(self, cell):
        """Get a set of all the neighbouring node cells."""
        return self.get_neighbouring_cells_in(cell, self.node_cells)
    
    ########################################################
    # --Paths layer.
    def _template_layer_creation(self, src_cell, dest_cell, neigh_callbk):
        
        # Cells in the same layer is of the same distance(from src_cell.)
        current_layer = [
            [src_cell]      # Layer 0
        ]
        
        # The 0th index is occupied by the source cell 
        # from where we are initiating the search.
        yield [src_cell]
        
        visited = [src_cell]
        new_cell_layer = [src_cell]
        
        # Iterate every Layer and find the neighbours of
        # the cells in those layer. The unvisited neighbours 
        # make up the next layer.
        
        while len(current_layer) > 0:
            if dest_cell in new_cell_layer: return
            cell_layer = current_layer.pop(0)
            neighbours = []
            
            # Gets all neighbours of the cells in that layer.
            for cell in cell_layer: neighbours += list(neigh_callbk(cell))
            neighbours = set(neighbours) 
            
            # The new layer should contain distinct 
            # elements that are not in the visited list.
            new_cell_layer = list(set(neighbours) - set(visited))
            
            # Test if its end of layer.
            if len(new_cell_layer) == 0: continue
            
            # Contain the new_cell_layer in current_layer.
            current_layer.append(new_cell_layer)
            
            # Generate the new layer as the next iteration.
            yield new_cell_layer
            
            visited += list(set(new_cell_layer) - set(visited))
            print neighbours
            
    def generate_depth_layers(self, dest_cell = None):
        """Group every cell with the same depth from source together."""
        return list(self._template_layer_creation(self.root_cell, dest_cell))
        
    def generate_distance_layers(self, src_cell, dest_cell = None):
        """Group every cell with the same depth from source together."""
        callback = self.get_neighbouring_node_cells
        return list(self._template_layer_creation(src_cell, dest_cell, callback))
        
    def generate_displacement_layers(self, src_cell, dest_cell = None):
        """Group every cell with the same displacement from source together."""
        callback = self.get_all_neighbouring_cells
        return list(self._template_layer_creation(src_cell, dest_cell, callback))
        
    ########################################################
    # --Distance / displacement / Depth.
    def _template_find_distance(self, src_cell, dest_cell, layer_callbk):
        """Get the displacement b/w two cells."""
        
        # Note: The index of the layer in which the destiation cell
        # is present in determines the shortest distance between it
        # and the source cell.
        
        # Get the distance layers.
        layer_list = list(layer_callbk(src_cell) )
        
        # Take every layer.
        for layer in layer_list:
            
            # Return the index of layer if cell is precent in it.
            if dest_cell in layer: return layer_list.index(layer)
            
    def get_cell_distance(self, src_cell, dest_cell):
        callbk = (self.generate_distance_layers)
        layers = self._template_find_distance(src_cell, dest_cell, callbk)
        return len(layers) - 1
        
    def get_cell_depth(self, cell):
        callbk = (self.generate_depth_layers)
        layers = self._template_find_distance(src_cell, dest_cell, callbk)
        return len(layers) - 1
        
    def get_cell_displacement(self, src_cell, dest_cell):
        callbk = self.generate_displacement_layers
        layers = self._template_find_distance(src_cell, dest_cell, callbk)
        return (layers) - 1
    
    ########################################################
    # --Cells at displacement / distance / depth.
    def get_all_cells_at_displacement(self, src_cell, displacement):
        """All cells in specific layer is returned."""
        disp_layers = list(self.generate_displacement_layers(src_cell))
        return disp_layers[displacement]
        
    def get_all_cells_at_distance(self, src_cell, distance):
        """Get a list of cells at specific distance from root cell."""
        dist_layers = list(self.generate_distance_layers(src_cell))
        return dist_layers[displacement]
    
    def get_all_cells_at_depth(self, depth):
        """Get a list of cells at specific distance from root cell."""
        layers = list(self.generate_depth_layers(self.root_cell))
        return layers[depth]
        
    # TODO: Need to take care of NoLinkWithRootNode.
    def nodify_cell(self, cell):
        if cell in self.free_cells:
            self.free_cells.remove(cell)
            self.node_cells.add(cell)
        else: print "Couldn't nidify cell"+str(cell)
            
    def nodify_cells_in_list(self, li):
        for cell in li: self.nodify_cell(cell)
            
    def nodify_cells_around_cell(self, cell):
        for cell in self.get_all_neighbouring_cells(cell): self.nodify_cell(cell)
    
    ########################################################
    def pick_any_free_cell(self):
        cell = random.choice(list(self.free_cells))
        return cell
    
    def test_cell_linkage(self, cell_1, cell_2):
        """Method to check whether node cell is reachable from root_cell."""
        connection = False
        scanned = [cell_1]
        
        for cell in scanned:
            cell_neighbours = list(self.get_neighbouring_node_cells(cell))
            scanned += list(set(cell_neighbours) - set(scanned))

            # Stop scanning as soon as the link is discovered.
            if cell_2 in scanned:
                connection = True
                break
            
        print cell_neighbours, "cell_neighbours"
        return connection
        
    def config_node_cells(self):
    
        print True if self.root_cell in self.node_cells else False
        
        node_cells = list(self.node_cells)
        print node_cells
        for index in range(len(node_cells)):
            while True:
                cell = node_cells[index]
                
                if self.test_cell_linkage(cell, self.root_cell):
                    print cell, "Tested and linked."
                    break
                
                else:
                    print "Found an unconnected cell", cell
                    node_cells[index] = self.pick_any_free_cell()
                    self.free_cells.add(cell)
                    self.free_cells.remove(node_cells[index])
                    
                    self.node_cells = set(node_cells)
                    
        self.node_cells = set(node_cells)
        
    def generate_node_lattice(self, nodes_count):
        
        # Generation of the basic structure.
        for r in range(self.max_r):
            for c in range(self.max_c):
                self.all_cells.add((r, c))
                self.free_cells.add((r, c))
        
        # restrain cells.
        
        # get root.
        self.root_cell = (0, 0)
        
        # From SinkCellHandler. # FIXME: Needs to be improved to predict true loops.
        self.assume_sink_cells(1, 4, affected_area=0, affect_type='C')
        self.assume_sink_cells(2, 4, affected_area=1, affect_type='C')
        
        self.assume_sink_cells(1, 4, affected_area=1, affect_type='C')
        self.assume_sink_cells(2, 6, affected_area=2, affect_type='C')
        
        # Draws the possible skeleton.
        for number in range(nodes_count):#56/2):
            
            cell = self.pick_any_free_cell()
            
            self.node_cells.add(cell)
            self.free_cells.remove(cell)
        
        self.config_node_cells()
        self.debug()
        
    def debug(self):
        arr = [[" " for c in range(self.max_c)] for r in range(self.max_r)]
        
        for scell_r, scell_c in self.sink_cells:
            arr[scell_r][scell_c] = "0"
        for fcell_r, fcell_c in self.free_cells:
            arr[fcell_r][fcell_c] = "*"
        for ncell_r, ncell_c in self.node_cells:
            arr[ncell_r][ncell_c] = "n"
        for vcell_r, vcell_c in self.void_cells:
            arr[vcell_r][vcell_c] = "v"
        
        display = ""
        
        for r in range(len(arr)):
            for c in range(len(arr[r])):
                display += "{:3}".format(arr[r][c])
            display += "\n"
        print display
        
class SinkCellHandler(): # Arbitrary. Needs rework.
    def __init__(self):
        self.sink_cells_list = []
        
    def assume_sink_cells(self, number_of_sinks, min_distance, max_distance=0, 
                                                affected_area=1, affect_type='C'):
        """Generates sinkcells that makes all neighbouring cells unusable."""

        # TODO: Analyse code for flaws...
        
        recent_sinks = []
        
        if len(self.sink_cells) == 0:
            first_sink=(random.randint(0, self.max_r-1),random.randint(0,self.max_c-1))
            self.sink_cells.add(first_sink)
            self.sink_cells_list.append(first_sink)
            
            recent_sinks = [self.sink_cells_list[-1]]
            
            # One sink is allready added.
            number_of_sinks -= 1
            
        queue_cell_to_remove = []
        cells_at_displacement = []
        
        for i in range(0, number_of_sinks):
            cells_at_displacement = []
            
            # Get all cells at the specified distace from the sink_cell.
            
            for sink_cell in self.sink_cells:
                cells_at_displacement += self.get_all_cells_at_displacement(sink_cell, min_distance)
                
            # Check whether every cell is atleast at a min_distance from the sink_cells.

            for cell in cells_at_displacement:
                
                for sink_cell in self.sink_cells:
                    if self.get_cell_displacement(cell, sink_cell) < min_distance: 
                        queue_cell_to_remove += [cell]
            cells_at_optimal_displacement = cells_at_displacement
            
            # Remove all cells that are put to remove queue.
            for cell_to_remove in queue_cell_to_remove:

                if cell_to_remove in cells_at_optimal_displacement: cells_at_optimal_displacement.remove(cell_to_remove)
            
            # Chose any one cell from the list of cells at optimal displacement.
            cells_at___ = cells_at_optimal_displacement
            if len(cells_at___):print len(cells_at___)
            else: 
                print "Cannot provide more free sinks..."
                return
            append = set([random.choice(cells_at_optimal_displacement)])
            self.sink_cells |= append
            self.sink_cells_list += append
            recent_sinks += [self.sink_cells_list[-1]]
            
        
        if affect_type == 'C':
            # The sinkcell's neighbours are discovered.
            for cell in recent_sinks:
                sink_disp_layer = list(self.generate_displacement_layers(cell) )
                
                for layer_index in range(0, affected_area + 1):
                    self.void_cells |= set(sink_disp_layer[layer_index])
                    
        elif affect_type == 'T':
            for sink in recent_sinks:
                
                top = random.choice([0, 1])
                
                for displacement in range(0, affected_area + 1):
                    raw_input(displacement)
                    cell_list = self.get_all_cells_at_displacement(sink, displacement)
                    
                    for cell in cell_list:
                        if (
                            (top and cell[0] + displacement <= sink[0])
                            or (not top and cell[0] >= sink[0] + displacement) 
                        ): 
                            self.void_cells.add(cell)
                    
        elif affect_type == 'D':
            for sink in recent_sinks:
                
                top = random.choice([0, 1])
                for displacement in range(0, affected_area + 1):
                
                    cell_list = self.get_all_cells_at_displacement(sink, displacement)
                    for cell in cell_list:
                        if (
                            (top and cell[0] <= sink[0])
                            or (not top and cell[0] >= sink[0])
                        ): self.void_cells.add(cell)
        
        elif affect_type == 'AV':
            for sink in recent_sinks:
                
                top = random.choice([0, 1])
                
                for displacement in range(1, affected_area + 1):
                
                    cell_list = self.get_all_cells_at_displacement(sink, displacement)
                    for cell in cell_list:
                        if (
                            (top and cell[0] <= sink[0])
                            or (not top and cell[0] >= sink[0])
                        ): self.void_cells.add(cell)
                        
        for cell_to_delete in self.void_cells:
            if cell_to_delete in self.free_cells: self.free_cells.remove(cell_to_delete)
            
class ShapeHandler():
    # TODO: in the next minor version.
    # Should be extened to AbstractSubsystemHandler.
    pass    
class ShapeContainer():
    pass
    
class ShapeSprite():
    def calculate_boundary(self):
        for cell in self.shape_cells:
            if self.get_neighbouring_node_cells(cell): yield cell
    
    def calculate_shape(self):
        s_cells = [self.starting_cell]
        for cell in shape_cells:
            s_cells += list(self.get_neighbouring_void_cells(cell) - set(s_cells))
        self.shape_cells = s_cells
        # TODO: Need to cut shapes.
        
class AbstractSubsystemHandler(object):
    #TODO: Make listing and indexing of subsystems(including non defensive
    # subsystems.).
    # TODO: Use ShapeHandler and ShapeContainer
    def __init__(self):
        self.subsystems_dict = {
            "FIREWALL" : set(),
            "ANTIVIRUS" : set(),
            "RESTORER" : set(),
            "SUPPRESSOR" : set(),
        }
    def get_cells_with_defined_connectivity(self, max_connectivity):
                
        # Stores which cells are possble to be assigned a Sub_System..
        compatible_cell_list = []
        for cell_tuple in self.all_cells:
            # FIXME: unnecessary dbl calculation of self.get_neighbouring_free_cells().
            neighbouring_cells_count = len(list(self.get_neighbouring_free_cells(cell_tuple)) )
            if neighbouring_cells_count <= max_connectivity and neighbouring_cells_count >=1:
                set_continue = False
                
                # Perform check operations before declaring it compatible,
                neighbour_list = list( self.get_neighbouring_free_cells(cell_tuple) )
                for neighbour_cell in neighbour_list:
                    if neighbour_cell in compatible_cell_list:
                        set_continue = True
                if set_continue: continue
                
                compatible_cell_list.append(cell_tuple)
        return compatible_cell_list
    
    def create_subsystems(self, firewall=0, antivirus=0, restorer=0, supressor=0, repair=0):
        
        firewall_set = set()
        antivirus_set = set()
        restorer_set = set()
        supressor_set = set()
        node_cells = set(self.get_node_cells())
        for f in range(firewall):
            firewall_set.add(random.choice(list(node_cells - firewall_set)))
        for a in range(antivirus):
            antivirus_set.add(random.choice(list(node_cells - firewall_set -antivirus_set)))
        for r in range(restorer):
            restorer_set.add(random.choice(list(node_cells - firewall_set - antivirus_set - restorer_set)))
        for s in range(supressor):
            supressor_set.add(random.choice(list(node_cells - firewall_set - antivirus_set - restorer_set - supressor_set)))
        self.subsystems_dict["FIREWALL"] = firewall_set
        self.subsystems_dict["ANTIVIRUS"] = antivirus_set
        self.subsystems_dict["RESTORER"] = restorer_set
        self.subsystems_dict["SUPPRESSOR"] = supressor_set
        
    def apply_subsystems_to_nodes(self):
        nodes = self.nodes()
        for cell in self.subsystems_dict["FIREWALL"]:
            self.get_node_by_cell(cell).set_container(FIREWALL)
        for cell in self.subsystems_dict["ANTIVIRUS"]:
            self.get_node_by_cell(cell).set_container(ANTIVIRUS)
        for cell in self.subsystems_dict["RESTORER"]:
            self.get_node_by_cell(cell).set_container(RESTORER)
        for cell in self.subsystems_dict["SUPPRESSOR"]:
            self.get_node_by_cell(cell).set_container(SUPPRESSOR)
        
class NodeCluster(CellFactory, ButtonGroup, PipeMethods, 
                                            AbstractSubsystemHandler, SinkCellHandler):
    """ Generates the Node structure and links every node to its respective neighbours.
    
    The draw method draws pipes and nodes.
        - generate_node - Prepares node based on the difficulty.#TODO: clear first.
        - connect_neighbours
    """    
    def __init__(self):
        CellFactory.__init__(self)
        PipeMethods.__init__(self)
        ButtonGroup.__init__(self)
        AbstractSubsystemHandler.__init__(self)
        SinkCellHandler.__init__(self)
        
        CellFactory.assign_diamension(self, (9, 12))
        CellFactory.generate_node_lattice(self, 56)###
        
        possible_root_cells = AbstractSubsystemHandler.get_cells_with_defined_connectivity(self, 3)
        self.root_cell = random.choice(possible_root_cells)
        PipeMethods.generate_pairs(self)
        
    def generate_node(self):
        """Creates node objects and links it to all its neighbouring nodes."""
        # Create nodes.
        # Init all nodes, connect them to their neighbours and root the root_cell.
        Primary_panel = Panel.get_primary()
        
        for cell in self.node_cells:
            node = Node(Primary_panel, cell)
            #node.set_container(SELF_REPAIR)
            ButtonGroup.add(self, node)
        # Connects node to neighbour.
        for node in self.nodes():
            self.connect_neighbours(node)
        self.get_node_by_cell(self.root_cell).root()
        
        # Assign Subsystems.
        AbstractSubsystemHandler.create_subsystems(self, 3,3,3,3, 2)
        AbstractSubsystemHandler.apply_subsystems_to_nodes(self)
        return self.nodes()
        
    def connect_neighbours(self, node):
        """Connects the provided node to its immediate neighbours."""
        # Changed. But slower.
        node.clear_linked()
        neighbouring_node_cells =CellFactory.get_neighbouring_node_cells(self,node.cell)
        for neighbouring_node_cell in neighbouring_node_cells:
            node.add_neighbours(self.get_node_by_cell(neighbouring_node_cell))
        return node.get_linked_neighbours()
        
    ###################################################################
    # Finders/Searchers.
    def get_node_by_cell(self, cell):
        """Searches for a node which belongs to the same cell."""
        nodes = self.nodes()
        for node in nodes:
            if cell == node.cell: return node
        # Returns last node if search fails.
        return node
    ###################################################################
    # Getters.
    def nodes(self):
        """nodes() get a list of nodes in the cluster."""
        return self.sprites()
    ###################################################################
    # Mutators.
    def feed(self, tooltip_spite):
        for sprite in self.sprites():
            sprite.feed(tooltip_spite)
    ###################################################################
    # Resetters.
    def reset_lattice(self):# TODO: Implement this.
        """Sets everything back to default."""
    def draw(self, surface):
        PipeMethods.draw(self, surface)
        ButtonGroup.draw(self, surface)
        
    def connect(self, system):
        self.system = system    
        nodes = self.nodes()
        for node in nodes:
            node.link_system(system)
            node.clicked(system.node_clicked_callback, (node, ))
            node.enter(system.node_enter_callback, (node,))
            node.leave(system.node_left_callback, (node,))
