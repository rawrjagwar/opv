# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray
"""

import pyvisa
import pymeasure
import time

from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2750

adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17

# beep the sourcemeter
sourcemeter.beep(420,0.2)

# set output to automatically turn on
sourcemeter.write(':SOURce:CLEAr:AUTO ON')
print(sourcemeter.output_off_state)


# sourcemeter sets a voltage and takes measurements
sourcemeter.source_voltage = 10
print(sourcemeter.voltage)
time.sleep(2)
sourcemeter.source_voltage = 0
print(sourcemeter.voltage)

# sourcemeter is reset and outputs are turned off
sourcemeter.reset()
time.sleep(2)

# switch system is reset with all channels opened
switchsystem.write(':open all')