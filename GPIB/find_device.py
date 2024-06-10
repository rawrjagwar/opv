# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray
"""

import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())

contr = rm.open_resource('ASRL3::INSTR') 
print(contr.query('*IDN?'))