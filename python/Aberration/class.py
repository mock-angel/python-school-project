NodeManager > NodeLattice

HackGraphics
HackEngine
Hack

NodeSprite
#LatticeSprites
System&Virus


"""
CELL - (r, c)
Cells are the co-ordinate unit of the nodes.  Its essential that all the 
processing be done using cells and be stored in seperate lists to identify 
their decided properties.

    Different types of cells- All
    - sink cells
    - void cells
    - free cells
    - node cells
    - root cell
    
SINK
A SINK creates a void space around itself depending on the pattern chosen.
    *   *   *   *   [* - free cell] (cells that can contain nodes.)
    *   *   v   *   [v - void cell] (cells affected by the sink cells)
    *   v   0   v   [0 - sink cell] (defines void cells.)
    *   v   v   v   
    
    free space - area containing the free cells.
    *   *   *   *
    *   *       *
    *
    *

    Pattern(n)
    *Pattern(1)                    *Pattern(2)
            v                               v
        v   0   v                       v   v   v
        v   v   v                   v   v   0   v   v
                                    v   v   v   v   v   
                                    v   v   v   v   v

    The Pattern is applied after the sink cell is chosen from the free space
    thats bordering the other sink patterns.
    
    
NODE
A node is the basic active unit in the game.  Its an extended button class
which also makes it a sprite object.  The user sees these nodes and interacts
with them during gameplay.

Special subsystem properties are given to the Node which can run special
(SEE subsystems)operations. 
    
    DRY nodes are not hackable.
    All nodes must be tagged wet to decrypt.
    
    
  SUBSYSTEMS
    TYPES:
    - Root Node
    
    WET
    - Antivirus
        - Antivirus Node
        - Core Node         [*Star node]
        - Firewall Node
        - Restorer Node
        - Supressor Node
    - Utility Subsystems.
        - Kernel Rot        [*Star node]
        - Polymorphic Shield[*Star node]
        - Self Repair       [*Star node]
        - Secondary Vector  [*Star node]
    *Star nodes.
        They are used to find the least number to be displayed during user 
        choice.
    Node.Group
    
    STATES:
    - Encrypted Node- not revealed      
        - inaccessible for clicked              DRY
        - accessible                            WET
    - Subsystem Node- revealed          
        -antivirus                      DEFENCE
        - utility+core                    HEAVY
    
    - Empty Node    - revealed                  HACKED
    - Disabled node by system                   POLARISED
        -core and datacache#, and utility
        
        
"""
"""
LatticeStructureGenerator
Is used by the NodeLattice class to generate the game marix.
    
    * cell_lattice_list - Contains all the cell locations in the form of tuples.
    * all_cells - Cords of all cells.
    * sink_cells - Stores all sink cell cordinares.
    * void_cells - Stores all void cell cordinates.
    * free_cells - List of all free cells that can be promoted to nodes.
    * node_cells - Lists that are to be promoted to nodes.
    
    # Finders/Searchers.
    
    
    # Setters
    

"""
#    * subsystem_list - Contains all the cell locations that's a subsystem. 
#        [Need to remove this.]
#Edge nodes
#Leaf node: a node with no children.
#Root node: a node distinguished from the rest of the tree nodes. Usually, it is depicted as the highest node of the tree.
#SINK cells help define voids in the lattice to generate a pattern.
#SINKperemeter is cells that belong to the peremeter of the SINK cells, i.e,
#    that are affected by the SINK cells.
#All the SINKcell 
@staticmethod
@classmethod
__metaclass__  = abc.ABCMeta
@abc.abstractmethod
VIRUS_SPECIAL = 
SYSTEM_SPECIAL
SPECIAL_ANY = VIRUS_SPECIAL + SYSTEM_SPECIAL

Node
    * cell_t
    * strength
    * coherence
    * linked_list           - Contains other nodes its linked to.
    * tag = DRY/WET/DRAINED
    * PROPERTY = EMPTY/
    * sub_property = NONE/SPECIAL_ANY
    
    # Getters.
    - get_linked_list()
    - get_linked_cells()
    - cell
    # Setters.
    - link_node(node)
    - link_system(system)
    - cell(cell)
    - clear_linked()
    # Operations.
    - drain()
#            will disable all the surrounding HEAVY nodes
#            wil dry all the surrounding WET nodes.
    - touch()
        #when a node is selected.
    - 
#TODO:  
LatticeStructureGenerator
    
    * all_cells
    * sink_cells
    * void_cells
    * free_cells
    * node_cells
    * root_cell
    
    # Setter.
    - assign_diamension(rc)
    
    # Getters.
    - get_sink_cells()
    - get_void_cells()
    - get_free_cells()
    - get_all_cells()
    - get_node_cells()
    
    # --Neighbour Calculation.
    - get_neighbouring_cells_in(cell, set_)
    - get_all_neighbouring_cells(cell)
    - get_neighbouring_free_cells(cell)
    - get_neighbouring_void_cells(cell)
    - get_neighbouring_node_cells(cell)
    
    # --Paths layer.
    - _template_layer_creation(src_cell, dest_cell, neigh_callbk)
    - generate_depth_layers(dest_cell = None)
    - generate_distance_layers(src_cell, dest_cell = None) 
    - generate_displacement_layers( src_cell, dest_cell = None) 
    
    # --Cell Distance calculaion# Distance / displacement.
    - _template_find_distance(src_cell, dest_cell, layer_callbk)
    - get_cell_distance(src_cell, dest_cell)
    - get_cell_depth(cell)
    - get_cell_displacement(src_cell, dest_cell)
    
    # --cells at displacement/distance
    - get_all_cells_at_displacement()
    
    
    
    # Sink cells generation.
    # Finding subsystem locations.
    - get_shortest_path(src_cell, dest_cell)# implementaion after sink_cells
    
    # Nodify.
    - nodify_cell(cell)
    - nodify_cells_in_list(li):
    - nodify_cells_around_cell(cell):
    
    - get_recommended_newcells()
    - choose_newcell()
    
    
    - generate_cell_board(node_count)
#TODO:    
NodeCluster(LatticeStructureGenerator, ButtonGroup)
    * 
    
    - generate_lattice()            
    - link_nodes_to_neighbours(node)  
    
    # Finders/Searchers.
    - get_node_using_cell(cell)
    
    # Getters.
    - nodes()
    
    # Resetters.
    - reset_lattice()
    
    
    
    
    
    
    
    
    
    
