# -*- coding: utf-8 -*-
"""
Created on Thu May 16 07:55:58 2024

@author: conor

Test script to operate switch system using variables. To be integrated into 
IV_curve_04.py at a later date.

switch system turns on three channels until triggered to close. This should be as 
repeatable as possible and ideally within a loop which can later integrate other 
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

# Instruments
adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17

# Switch System Variables
cell_1_ch = '1!1, 1!2' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2_ch = '1!3, 1!4' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3_ch = '1!5, 1!6' # channels 5 & 6 - pins
test_cells_ch = [cell_1_ch, cell_2_ch, cell_3_ch]

# Switch System Setup
switchsystem.write(':open all')
switchsystem.write('*RST')

# Sleep loop variables
sleep_1 = 3
sleep_2 = 5
sleep_loop = [sleep_1, sleep_2]

for ch in test_cells_ch:
    switchsystem.write(':clos (@ '+ ch + ')')
    for z in sleep_loop:
        print('zzz')
        sleep(z)
    switchsystem.write(':open (@ '+ ch + ')')
    sleep(2)
    
switchsystem.write(':open all')
