# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:40:19 2024

@author: conor
"""

import sys,os
sys.path.append(os.getcwd())

def variable_A():
    from test_loop_print_gui import VAR_A
    print(VAR_A[0])


#if __name__ == '__main__':
variable_A()