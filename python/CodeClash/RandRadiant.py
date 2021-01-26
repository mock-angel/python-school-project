#RandRadiant v1.0

from ChatFns import randomize, lim_rand
import random

class RandRadiant():
    def __init__(self):

        #                  RTree:
        #
        #   Branch1        Branch2         Branch3
        # element.0.1    element.1.1     element.2.1
        # element.0.2    element.1.2     element.2.2
        # element.0.3    element.1.3     element.2.3
        
        self.RTree = []
        
    # Tree OPS #########
    def clear_tree(self):
        self.RTree = []
    
    def clear_tree_element(self, SelElement):
    
        # Search for Element and delete it entirely.
        Count = 0
        for Element in self.RTree:
            if (Element[0])==str(SelElement): del self.RTree[Count]
            Count += 1
    
        # Read the element as blank to grid.
        self.create_new_branch(SelElement)
        
    def create_new_branch(self, NewBranch):
        
        # Add a new Element To Grid.
        self.RTree += [[str(NewBranch)]]
        
    # Elem OPS #########
    def del_element_from_branch(self, Element, Branch):
        ElementCount = 0
        ValueCount = 0
        RGL = len(self.RTree)
        
        self.DisplayAll()
        
        BIndex = self.__get_branch_index(Branch)
        EIndex = self.__get_element_index_from_branch(Element, BIndex)
        
        del self.RTree[BIndex][EIndex]
        
    def __get_branch_index(self, Branch):                     # NotTested.
        count = 0
        for List in self.RTree:
        
            if List[0]==Branch: return count
            else: count += 1
            
    def __get_element_index_from_branch(self, Element, BIndex): # NotTested.
        count = 0
        for E in self.RTree[BIndex]:
            if E==Element: return count
            else: count += 1
        
    
        
    def add_element_to_branch(self, Element, Branch):
    
        BIndex = self.__get_branch_index(Branch)
        
        self.RTree[BIndex] += [Element]
        
    def write_random_number_to_branch_by_digit(self, Digits, Branch):
        ElementCount = 0
        
        BIndex = self.__get_branch_index(Branch)
        
        while True:
          RandomNumber = randomize(Digits)
          
          if str(Val) in self.RandomGrid[BIndex][1:]: 
            continue
          else: 
            self.RandomGrid[BIndex] += [str(RandomNumber)]
            return str(Val)
            
    def write_random_number_to_branch_by_range(self, limitTuple, Branch):
        
        BIndex = self.__get_branch_index(Branch)
        print limitTuple[1] - limitTuple[0], len(self.RTree[BIndex][1:])
        if limitTuple[1] - limitTuple[0]<len(self.RTree[BIndex][1:]): return
        
        while True:
          RandomNumber = lim_rand(limitTuple[0], limitTuple[1])
          
          if str(RandomNumber) in self.RTree[BIndex][1:]: 
            continue
          else: 
            self.RTree[BIndex] += [str(RandomNumber)]
            return str(RandomNumber)
            
    def write_random_number_to_branch_by_choice(self, choice_list, Branch):
        
        BIndex = self.__get_branch_index(Branch)
        if len(choice_list)<=len(self.RTree[BIndex][1:]): return
        
        while True:
          RandomNumber = random.choice(choice_list)
          
          if str(RandomNumber) in self.RTree[BIndex][1:]: 
            continue
          else: 
            self.RTree[BIndex] += [str(RandomNumber)]
            return str(RandomNumber)
            
    def DisplayAll(self):
        Display = ""
        for i in self.RTree:
            for j in i:
                Display += "{:5}".format(str(j))
            Display += "\n"
        print Display
        
if __name__ == "__main__":
    test = RandRadiant()
    test.create_new_branch("Branch#1")
    test.create_new_branch("Branch#2")
    test.write_random_number_to_branch_by_range((0,18), "Branch#2")
    #test.DelElementFromBranch("6", "Branch#1")
    #test.ClearTreeElement("Branch#1")
    test.DisplayAll()
