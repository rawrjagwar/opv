# -*- coding: utf-8 -*-
"""
Created on Wed May 29 09:04:50 2024

@author: coray
"""

import pyvisa
import pymeasure
from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400

# Instruments
adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24

sourcemeter.write(":syst:beep:stat 0")

sourcemeter.write(":syst:beep:stat?")

print(sourcemeter.read())

sourcemeter.reset()

sourcemeter.write(":syst:beep:stat?")

print(sourcemeter.read())