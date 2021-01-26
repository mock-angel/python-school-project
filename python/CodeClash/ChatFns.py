#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# ChatFns.py

"""
 *
 * Authors: Anantha Krishna R. 
 *
"""

'''
                    2017-12-26  STALLED
'''

import os.path
import random

def randomize(length):


    while True:
        RanNum = int(random.random() * (10**length))
        
        if len(str(RanNum)) == length: return RanNum
    
def lim_rand(ml, mh, mm=1):

        minl = (ml / mm) 
        
        maxl = (mh / mm) 
        
        if (minl*2) < ml: minl += 1

        RanNum = int(random.randint(minl, maxl))  * mm
            
        return RanNum

if __name__ == "__main__":
    # Test.
    
    upper_limit = 11
    lower_limit = 23
    mul = 2
    
    print [(lim_rand(upper_limit, lower_limit, mul)) for x in range(0,10)]
