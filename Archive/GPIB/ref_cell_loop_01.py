# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:26:49 2024

@author: coray

Loop to measure the resistance of the reference cell i.e. the temperature
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
cell_1 = '1!1, 1!2' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2 = '1!3, 1!4' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3 = '1!5, 1!6' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
ref_cell = '1!7, 1!8' # channels
temp = '' # channels 
test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4', cell_3 : '1!5, 1!6'}

# Switch System Setup
switchsystem.write(':open all')
switchsystem.write('*RST')

for ch in test_ch:
    switchsystem.write(':clos (@ '+ ref_cell + ')')
    sleep(0.1)
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    sourcemeter.measure_voltage()
    sourcemeter.enable_source()
    print(sourcemeter.voltage) # This variable should be exported to a dataframe
    sourcemeter.disable_source()
    switchsystem.write(':open (@ '+ ref_cell + ')')
    sleep(0.1)
    
sourcemeter.shutdown()