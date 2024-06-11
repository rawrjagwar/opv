# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:40:40 2024

@author: conor
"""
import sys,os
sys.path.append(os.getcwd())



def loop():
    from test_loop_print_var import VAR_A
    print(VAR_A[0])
    
if __name__ == '__main__':
    loop()