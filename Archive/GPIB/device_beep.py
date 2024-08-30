# -*- coding: utf-8 -*-
"""
Created on Tue Apr  19 11:37:48 2024

@author: Conor Brisco Ray

checks whether an instrument is connected through pyvisa and tests communication
"""

import pyvisa

rm = pyvisa.ResourceManager()

# create controller variable
contr = rm.open_resource('ASRL3::INSTR') 

# set GPIB address as 24 as default
if contr.query('++addr') != 24:
    contr.write('++auto 0')
    contr.write('++addr 24')

# set controller to write
contr.write('++auto 0')
contr.write(':SYSTem:BEEPer 420, 1')

contr.write(':SYSTem:BEEPer 210, 1')