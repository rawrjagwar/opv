# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray
"""

import pyvisa
import pymeasure

from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2000

rm = pyvisa.ResourceManager()
print(rm.list_resources())

adapter = PrologixAdapter('ASRL3::INSTR', address=24)
sourcemeter = Keithley2400(adapter)  # at GPIB address 24
multimeter = Keithley2000(adapter.gpib(17))  # at GPIB address 17

sourcemeter.id

#contr = rm.open_resource('ASRL3::INSTR') 
#print(contr.query('*IDN?'))