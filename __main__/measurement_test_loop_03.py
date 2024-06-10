# -*- coding: utf-8 -*-
"""Created on Mon June 3 13:27:14 2024

@author: conor

Automated measurement program for OPV Solar Cells from ASCA for the TH Köln.

Cycles through each connected Cell and creates an IV-Curve for each from which 
the Maximum Power Point, Open Circuit Voltage and Short Circuit Current can be 
calculated. These values are then used to calculate the Fill Factor. For each 
cell cycle Irradiation and Temperature measurements are taken using a Reference 
Solar Cell. Together with these measurements the Efficency can be calculated.

Implementation of wakepy to automatically stop the CPU from turning off during 
measurements.
"""

# Packages
import os
import pyvisa
import pymeasure
import numpy as np
import pandas as pd
import math
import time
from time import sleep
from wakepy import keep
from pymeasure.adapters import PrologixAdapter
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2750
from datetime import datetime

print('initialising opv measurements')

# Instruments
adapter = PrologixAdapter('ASRL3::INSTR')
sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17

# Variables
data_points = 50
averages = 10
max_voltage = 0 # in Volts
min_voltage = -25 # in Volts

print('cells will be measured up to a voltage of:',abs(min_voltage),'V')

# Efficiency Calculation Constants
ref_power = 104.749 # mV / W/m²
stc_power = 1000 # W/m²
cell_area = 0.0075 # m²

# Temperature Calculation Constants
res_0 = 1000
temp_a = 0.0039083
temp_b = -0.0000005775

# Switch System Variables
cell_1 = 'cell_1' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
cell_2 = 'cell_2' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
cell_3 = 'cell_3' # channels 5 & 6 - pins 2a, 3a, 4a and 5a

test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4', cell_3 : '1!5, 1!6'}

ref_cell = '1!7, 1!8' # channels 7 & 8 - pins 21a, 18a, 8a and 10a
temp_sensor = '1!9, 1!10' # channels 9 & 10 - pins 4b, 5b, 12b and 11b

# Parameters
voltage_range = 25 # in Volts
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

# Create an empty dataframe to collect all results outside the loop
final = pd.DataFrame()

# Path to save results
path = r'C:\Users\coray\Documents\GitHub\opv\__main__'

# Set the time for the measurement session
hours = 0
minutes = 5

# Calculates the total time in seconds
timeout = (hours * 3600) + (minutes * 60) # seconds
print ('measurements will run for:', hours, 'hour(s) and', minutes, 'minute(s)')

# Sets the initial time value when the program is started
timeout_start = time.time()

print('starting measurement cycle...')

# counter to track measurement cycles
counter = 0

# wakepy module to stop CPU from sleeping during measurements
with keep.running():
    # Creates a countdown within which the measurement loop should be integrated
    while time.time() < timeout_start + timeout:
        # Main loop cycling through each cell to create IV-curve measurements
        for ch in test_ch:
            switchsystem.write(':clos (@ '+ test_ch[ch] + ')')
            sourcemeter.reset()
            sourcemeter.write(":syst:beep:stat 0") # Disabling the beeper on the sourcemeter
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
            switchsystem.write(':open (@ '+ test_ch[ch] + ')')
            sleep(0.1)
            
            # Reference Solar Cell loop
            switchsystem.write(':clos (@ '+ ref_cell + ')')
            sleep(0.1)
            sourcemeter.reset()
            sourcemeter.write(":syst:beep:stat 0") # Disabling the beeper on the sourcemeter
            sourcemeter.use_front_terminals()
            sourcemeter.measure_voltage()
            sourcemeter.enable_source()
            ref_sig = sourcemeter.voltage # This variable should be exported to a dataframe
            sourcemeter.disable_source()
            switchsystem.write(':open (@ '+ ref_cell + ')')
            
            # Temperature loop
            switchsystem.write(':clos (@ '+ temp_sensor + ')')
            sleep(0.1)
            sourcemeter.reset()
            sourcemeter.write(":syst:beep:stat 0") # Disabling the beeper on the sourcemeter
            sourcemeter.use_front_terminals()
            sourcemeter.measure_resistance()
            sourcemeter.enable_source()
            temp_res = sourcemeter.resistance # This variable should be exported to a dataframe
            sourcemeter.disable_source()
            switchsystem.write(':open (@ '+ temp_sensor + ')')
            sleep(0.1)  
            
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
            voc = min_current['Voltage (V)'].to_list()[0] # in V
            min_current = min_current['Current (A)'].to_list()[0]
            isc = data.iloc[data['Current (A)'].argmax()]['Current (A)'] # in A
    
            # Calculating the power produced by the system to find the MPP
            # Create Power column and populate
            data['Power (W)'] = data['Voltage (V)'] * data['Current (A)']
            # Find the MPP Value in W
            mpp = data.iloc[data['Power (W)'].argmax()]['Power (W)'] # in W
    
            # Calculate the Fill Factor
            ff = mpp/(isc*voc)
    
            # Calculate the reference solar cell irradiation
            irradiation = (ref_sig*1000 / ref_power)*stc_power # in W/m²
    
            # Calculate the efficiency of the cell
            eff = 100 * (mpp / (cell_area * irradiation)) # in %
            
            # Calculate the temperature from the resistance 
            temp = (-temp_a + math.sqrt((temp_a**2)-(4*temp_b*(1-(temp_res/res_0)))))/(2*temp_b) # in °C
            
            # Create a dictionary for the results
            results = {"Timestamp" : [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "Cell" : [ch],
                    "Isc" : [isc],
                    "Voc" : [voc],
                    "MPP" : [mpp],  
                    "FF" : [ff],
                    "Irradiation" : [irradiation],
                    "Efficiency" : [eff],
                    "Temperature" : [temp]
                    }
            # Convert to a DataFrame
            results_df = pd.DataFrame(data = results)
            # Export to final results DataFrame
            final = pd.concat([final,results_df], ignore_index = True)
            # log the measurement cycle to the counter
            counter += 1
            print('number of measurements completed:',counter)

print('measurement cycle complete \nwriting measurement results to csv file...')
# Save data to a csv file
final.to_csv(os.path.join(path,'measurement_test_loop_03.csv'))

print('results successfully saved\nfile path:',
      os.path.join(path,'measurement_test_loop_03.csv'))
# Reset switch system and sourcemeter
switchsystem.write(':open all')
switchsystem.write('*RST')
sourcemeter.shutdown()

print('all instruments successfully shutdown \nmeasurement session ended')