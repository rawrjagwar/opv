# -*- coding: utf-8 -*-
"""
Created on Tue Apr  19 11:37:48 2024

@author: Conor Brisco Ray

checks whether an instrument is connected through pyvisa and tests communication
"""

import pyvisa

rm = pyvisa.ResourceManager()

print(rm.list_resources())

# create SourceMeter reference
sm = rm.open_resource('ASRL3::INSTR') 
# string should contain Instrument ID similar to 'USB0::0x1AB1::0x0E11::DP8C1234567890::INSTR'
# currently with placeholder reference of the controller port

# asking SourceMeter for identification
print(sm.query("*IDN?"))
