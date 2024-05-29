# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:26:43 2024

@author: conor

Time loop to control the overall loop. Set the time limit in hours and minutes.

"""

import time

# Set the time for the measurement session
hours = 0
minutes = 1

# Calculates the total time in seconds
timeout = (hours * 3600) + (minutes * 60) # seconds
print (timeout)

# Sets the initial time value when the program is started
timeout_start = time.time()

# Creates a countdown within which the measurement loop should be integrated
while time.time() < timeout_start + timeout:
    print('working...')
    time.sleep(5)