# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray
"""

import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
