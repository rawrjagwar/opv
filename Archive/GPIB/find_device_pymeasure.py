# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray

Test to find connected devices with the Prologix Adapter and print their IDs

Keithley 2700 used as placeholder for 7000 Series Switch System
"""

import pyvisa
import pymeasure

from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2700

adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2700(adapter.gpib(17))  # at GPIB address 17

print(sourcemeter.id)
print(switchsystem.id)
