# Helper.py
def append_nonduplicates(list1, list2):
    
    for element in list2:
        #print element
        if (element in list1): 
            pass
        else:
            list1.append(element)
    return list1
    
def list2d(Tuple=(0,0), value=0):
    return [[value for col in range(Tuple[1])] for row in range(Tuple[0])]  
