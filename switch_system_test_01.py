# -*- coding: utf-8 -*-
"""
Created on Thu May 16 07:55:58 2024

@author: conor

Test script to operate switch system using variables. To be integrated into 
IV_curve_04.py at a later date.

switch system turns on two channels until triggered to close. This should be as 
repeatable as possible and ideally within a loop which can later integraee other 
cells. The loop for the IV curve should be possible to place inside the switch 
loop.
"""

# Packages
import pyvisa
import pymeasure
import numpy as np
import pandas as pd
from time import sleep
from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2750
'''
# Instruments
adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17
'''
# Switch System Variables
cell_1_ch = '1!1, 1!2' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2_ch = '1!3, 1!4'
test_cells_ch = [cell_1_ch, cell_2_ch]
'''
# Switch System Setup
switchsystem.write(':disp:enab: OFF')
switchsystem.write(':open all')
switchsystem.write('*RST')
'''

# Sleep loop variables
sleep_1 = 3
sleep_2 = 5
sleep_loop = [sleep_1, sleep_2]

for i in test_cells_ch:
    print(':clos (@',i + ')')
    for j in sleep_loop:
        print('zzz')
        sleep(j)
    print(':open (@',i + ')')
    sleep(2)