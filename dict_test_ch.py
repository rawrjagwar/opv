# -*- coding: utf-8 -*-
"""
Created on Mon May 27 20:27:25 2024

@author: conor
"""
from datetime import datetime
from time import sleep

cell_1 = 'cell_1' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2 = 'cell_2' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3 = 'cell_3' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
ref_cell = '1!7, 1!8' # channels 7 & 8 - pins 21a, 18a, 8a and 10a
temp = '1!9, 1!10' # channels 9 & 10 - pins 4b, 5b, 12b and 11b
test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4', cell_3 : '1!5, 1!6'}
isc = 'isc'
voc = 'voc'
mpp = 'mpp'
ff = 'ff'
irradiation = 'irradiation'
eff = 'efficiency'

for ch in test_ch:
    print(ch)
    print(':clos (@ '+ test_ch[ch] + ')')
    

    results = {"Timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Cell" : ch,
        "Isc" : isc,
        "Voc" : voc,
        "MPP" : mpp,  
        "FF" : ff,
        "Irradiation" : irradiation,
        "Efficiency" : eff
        }
    
    print(results)
    sleep(1)