# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray

Script to create an IV-Curve for one cell and calculate the MPP from the data 
produced.

Runs one cell through the 7001 Switch System. Closing two channels to 
measure and then opening them again after completion

Temperature Calculations
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
from datetime import datetime

# Instruments
adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17

# Variables
data_points = 50
averages = 10
max_voltage = 0 # in Volts
min_voltage = -14 # in Volts

# Calculation Constants
ref_power = 104.749 # mV / W/m²
stc_power = 1000 # W/m²
cell_area = 0.0075 # m²
ref_sig = 0.000919 # V
temp = 22 # dummy value

# Switch System Variables
cell_1 = 'cell_1' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2 = 'cell_2' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3 = 'cell_3' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
ref_cell = '1!7, 1!8' # channels 7 & 8 - pins 21a, 18a, 8a and 10a
temp_sensor = '1!9, 1!10' # channels 9 & 10 - pins 4b, 5b, 12b and 11b
test_ch = {cell_1 : '1!1, 1!2'}

# Parameters
voltage_range = 14 # in Volts
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
for ch in test_ch:
    switchsystem.write(':clos (@ '+ test_ch[ch] + ')')
    for i in range(data_points):
        sourcemeter.config_buffer(averages)
        sourcemeter.source_voltage = voltages[i]
        sourcemeter.start_buffer()
        sourcemeter.wait_for_buffer()
        # Record the average and standard deviation
        currents[i] = sourcemeter.mean_current
        sleep(0.01)
        current_stds[i] = sourcemeter.standard_devs[1]
    switchsystem.write(':open (@ '+ test_ch[ch] + ')')
    sleep(2)
    
    # Create dataframe to save results
    data = pd.DataFrame({
        'Voltage (V)': voltages,
        'Current (A)': currents,
        'Current Std (A)': current_stds,
    })

    # Convert Voltages to positive
    data['Voltage (V)'] = data['Voltage (V)'].abs()

    # Finding the max. voltage where the current is closest to zero
    min_current = data.iloc[data['Current (A)'].abs().argsort()[:1]]
    voc = min_current['Voltage (V)'].to_list()[0]
    min_current = min_current['Current (A)'].to_list()[0]
    isc = data.iloc[data['Current (A)'].argmax()]['Current (A)']

    # Calculating the power produced by the system to find the MPP
    # Create Power column and populate
    data['Power (W)'] = data['Voltage (V)'] * data['Current (A)']
    # Find the MPP Value in W
    mpp = data.iloc[data['Power (W)'].argmax()]['Power (W)']

    # Calculate the Fill Factor
    ff = mpp/(isc*voc)

    # Calculate the reference solar cell irradiation
    irradiation = (ref_sig*1000 / ref_power)*stc_power

    # Calculate the efficiency of the cell
    eff = mpp / (cell_area * irradiation)
    
    # Calculate the temperature from the resistance
    
    
    # Create a dictionary for the results
    results = {"Timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Cell" : ch,
            "Isc" : isc,
            "Voc" : voc,
            "MPP" : mpp,  
            "FF" : ff,
            "Irradiation" : irradiation,
            "Efficiency" : eff,
            "Temperature" : temp
            }
    
    # Next step will be to output these results to a dataframe and concatenate
    print(results)    


sourcemeter.shutdown()