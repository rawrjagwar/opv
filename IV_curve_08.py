# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray

Script to create an IV-Curve for three cells and calculate the required values 
for end results: Isc, Vmax, MPP, Fill Factor and eventually the Efficiency

Runs three cells through the 7001 Switch System. Closing 6 channels to 
measure and then opening them again after completion

Voltages set to lower value and fewer data points for quicker testing

Integrated temperature loop to record temp for each cell.
Created new channel references for the reference cell and temperature sensor
Integrated reference cell loop to record the mV signal
"""

# Packages
import pyvisa
import pymeasure
import numpy as np
import pandas as pd
from time import sleep
from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2750

# Instruments
adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17

# Variables
data_points = 10
averages = 10
max_voltage = 0 # in Volts
min_voltage = -0 # in Volts

# Switch System Variables
cell_1 = '1!1, 1!2' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2 = '1!3, 1!4' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3 = '1!5, 1!6' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
ref_cell = '1!7, 1!8' # channels 7 & 8 - pins 21a, 18a, 8a and 10a
temp = '1!9, 1!10' # channels 9 & 10 - pins 4b, 5b, 12b and 11b
test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4', cell_3 : '1!5, 1!6'}

# Parameters
voltage_range = 2 # in Volts
compliance_current = 25e-03  # in Amps
measure_nplc = 0.1  # Number of power line cycles
current_range = 25e-03  # in Amps

# Switch System Setup
switchsystem.write(':open all')
switchsystem.write('*RST')

# Create Arrays for Results
voltages = np.linspace(max_voltage, min_voltage, num=data_points)
currents = np.zeros_like(voltages)
current_stds = np.zeros_like(voltages)

# Main loop cycling through each cell to create IV-curve measurements
for ch in test_ch:
    switchsystem.write(':clos (@ '+ ch + ')')
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    sourcemeter.apply_voltage(voltage_range, compliance_current)
    sourcemeter.measure_current(measure_nplc)
    sleep(0.1)  # wait here to give the instrument time to react
    sourcemeter.stop_buffer()
    sourcemeter.disable_buffer()
    sourcemeter.enable_source()
    for i in range(data_points):
        sourcemeter.config_buffer(averages)
        sourcemeter.source_voltage = voltages[i]
        sourcemeter.start_buffer()
        sourcemeter.wait_for_buffer()
        # Record the average and standard deviation
        currents[i] = sourcemeter.mean_current
        sleep(0.01)
        current_stds[i] = sourcemeter.standard_devs[1]
    switchsystem.write(':open (@ '+ ch + ')')
    sleep(0.1)
    
    # Reference Solar Cell loop
    switchsystem.write(':clos (@ '+ ref_cell + ')')
    sleep(0.1)
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    sourcemeter.measure_voltage()
    sourcemeter.enable_source()
    ref_sig = sourcemeter.voltage # This variable should be exported to a dataframe
    sourcemeter.disable_source()
    switchsystem.write(':open (@ '+ ref_cell + ')')
    
    # Temperature loop
    switchsystem.write(':clos (@ '+ temp + ')')
    sleep(0.1)
    sourcemeter.reset()
    sourcemeter.use_front_terminals()
    sourcemeter.measure_resistance()
    sourcemeter.enable_source()
    temp_res = sourcemeter.resistance # This variable should be exported to a dataframe
    sourcemeter.disable_source()
    switchsystem.write(':open (@ '+ temp + ')')
    sleep(0.1)  

# Save data to a csv file
#data.to_csv('example_pandas_concat.csv')

 # Reset switch system and sourcemeter
switchsystem.write(':open all')
switchsystem.write('*RST')
sourcemeter.shutdown()