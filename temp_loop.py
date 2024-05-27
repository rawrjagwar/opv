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



sourcemeter.reset()
sourcemeter.use_front_terminals()

# Activate Output of Sourcemeter
sourcemeter.measure_resistance()
sourcemeter.enable_source()
print(sourcemeter.resistance)

sourcemeter.disable_source()

for ch in test_ch:
    switchsystem.write(':clos (@ '+ ch + ')')
    sourcemeter.measure_resistance()
    sourcemeter.enable_source()
    print(sourcemeter.resistance)
    sleep(0.01)
    switchsystem.write(':open (@ '+ ch + ')')
    sleep(2)  