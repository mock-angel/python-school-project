# -*- coding: utf-8 -*-
# CleanUp.py - v1.0

'''
                    2018-01-14  COMPLETED
'''

import os
def clean():
    os.system('find . -name "*.pyc" -type f -delete')
    os.system('cd ../libs && find . -name "*.pyc" -type f -delete')
    os.system('cd . && find . -name "*.pdf" -type f -delete')
#END

