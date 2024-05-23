# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:20:18 2024

@author: coray

Test Script to change the variables of the test cells to a dictionary for 
better looping
"""

# Switch System Variables
cell_1 = '1!1, 1!2' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2 = '1!3, 1!4' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3 = '1!5, 1!6' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
ref_cell = '' # channels
temp = '' # channels 
test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4', cell_3 : '1!5, 1!6'}

for ch in test_ch:
    print((':clos (@ '+ ch + ')'))