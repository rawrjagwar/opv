# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:54 2024

@author: coray
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
data_points = 46
averages = 10
max_voltage = 23 # in Volts
min_voltage = 0 # in Volts

# Parameters
voltage_range = 0 # in Volts
compliance_current = 10E-3  # in Amps
measure_nplc = 0.1  # Number of power line cycles
current_range = 10E-3  # in Amps

# Configure the Sourcemeter
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.apply_voltage(voltage_range, compliance_current)
sourcemeter.measure_current(measure_nplc, current_range)
sleep(0.1)  # wait here to give the instrument time to react
sourcemeter.stop_buffer()
sourcemeter.disable_buffer()

# Create Arrays for Results
voltages = np.linspace(min_voltage, max_voltage, num=data_points)
currents = np.zeros_like(voltages)
current_stds = np.zeros_like(voltages)

# Activate Output of Sourcemeter
sourcemeter.enable_source()

# Loop through each current point, measure and record the voltage
for i in range(data_points):
    sourcemeter.config_buffer(averages)
    sourcemeter.source_current = voltages[i]
    sourcemeter.start_buffer()
    sourcemeter.wait_for_buffer()
    # Record the average and standard deviation
    currents[i] = sourcemeter.means[0]
    sleep(1.0)
    current_stds[i] = sourcemeter.standard_devs[0]

# Save the data columns in a CSV file
data = pd.DataFrame({
    'Voltage (V)': voltages,
    'Current (A)': currents,
    'Current Std (A)': current_stds,
})
data.to_csv('example.csv')

sourcemeter.shutdown()