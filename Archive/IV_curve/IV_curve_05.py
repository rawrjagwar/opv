# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray

Script to create an IV-Curve for three cells.

Runs three cells through the 7001 Switch System. Closing 6 channels to 
measure and then opening them again after completion

Voltages set to lower value and fewer data points for quicker testing

Data is now saved into separate csv files. This should be amalgamated into a 
single dataframe outside of the loop and then the csv file created from that.
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
min_voltage = -2 # in Volts

# Switch System Variables
cell_1_ch = '1!1, 1!2' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2_ch = '1!3, 1!4' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3_ch = '1!5, 1!6' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
test_cells_ch = [cell_1_ch, cell_2_ch, cell_3_ch]

# Parameters
voltage_range = 2 # in Volts
compliance_current = 25e-03  # in Amps
measure_nplc = 0.1  # Number of power line cycles
current_range = 25e-03  # in Amps

# Switch System Setup
switchsystem.write(':open all')
switchsystem.write('*RST')

# Configure the Sourcemeter
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.apply_voltage(voltage_range, compliance_current)
sourcemeter.measure_current(measure_nplc)
sleep(0.1)  # wait here to give the instrument time to react
sourcemeter.stop_buffer()
sourcemeter.disable_buffer()

# Create Arrays for Results
voltages = np.linspace(max_voltage, min_voltage, num=data_points)
currents = np.zeros_like(voltages)
current_stds = np.zeros_like(voltages)

# Activate Output of Sourcemeter
sourcemeter.enable_source()

# Loop through each current point, measure and record the voltage
for ch in test_cells_ch:
    switchsystem.write(':clos (@ '+ ch + ')')
    for i in range(data_points):
        sourcemeter.config_buffer(averages)
        sourcemeter.source_voltage = voltages[i]
        sourcemeter.start_buffer()
        sourcemeter.wait_for_buffer()
        # Record the average and standard deviation
        currents[i] = sourcemeter.mean_current
        sleep(0.01)
        current_stds[i] = sourcemeter.standard_devs[1]
        # Save the data columns in a CSV file
        data = pd.DataFrame({
            'Voltage (V)': voltages,
            'Current (A)': currents,
            'Current Std (A)': current_stds,
        })
        # Save data to a csv file
        data.to_csv('example_'+ch+'.csv')
    switchsystem.write(':open (@ '+ ch + ')')
    sleep(2)    



 # Reset switch system and sourcemeter
switchsystem.write('*RST')
sourcemeter.shutdown()