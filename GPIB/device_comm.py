# -*- coding: utf-8 -*-
"""
Created on Tue Apr  19 11:37:48 2024

@author: Conor Brisco Ray

checks whether an instrument is connected through pyvisa and tests communication
"""

import pyvisa

rm = pyvisa.ResourceManager()

print(rm.list_resources())

# create controller as variable
contr = rm.open_resource('ASRL3::INSTR') 

# set GPIB address as 24 as default
if contr.query('++addr') != 24:
    contr.write('++auto 0')
    contr.write('++addr 24')

# asking SourceMeter for identification this should be the Sourcemeter
contr.write('++auto 1')
print(contr.query('*IDN?'))

# set the GPIB address of the controller to the switch system
contr.write('++auto 0')
contr.write('++addr 17')

# asking Switch System for identification
contr.write('++auto 1')
print(contr.query('*IDN?'))
