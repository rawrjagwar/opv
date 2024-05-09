# -*- coding: utf-8 -*-
"""
Created on Tue Apr  19 11:37:48 2024

@author: Conor Brisco Ray

checks whether an instrument is connected through pyvisa and tests communication

added new line to the end of every command for the controller
"""

import pyvisa

rm = pyvisa.ResourceManager()

print(rm.list_resources())

# create controller as variable
contr = rm.open_resource('ASRL3::INSTR') 

# set GPIB address as 24 as default
if contr.query('++addr \n') != 24:
    contr.write('++auto 0 \n')
    contr.write('++addr 24 \n')

# asking SourceMeter for identification this should be the Sourcemeter
contr.write('++auto 1 \n')
print(contr.query('*IDN?'))

# set the GPIB address of the controller to the switch system
contr.write('++auto 0 \n')
contr.write('++addr 17 \n')

# asking Switch System for identification
contr.write('++auto 1 \n')
print(contr.query('*IDN?'))
