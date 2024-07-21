# -*- coding: utf-8 -*-
"""
Organic Photovoltaic Automated Measurement Program (OPV AMP)

Automated measurement program for OPV Solar Cells from ASCA for the TH Köln.

Developed as part of a Master's Thesis researching the power and suitability of 
organic solar cells for the application in an active building facade designed to 
cool and heat the building.

Cycles through each connected Cell and creates an IV-Curve for each from which 
the Maximum Power Point, Open Circuit Voltage and Short Circuit Current can be 
calculated. These values are then used to calculate the Fill Factor. For each 
cell cycle Irradiation and Temperature measurements are taken using a Reference 
Solar Cell. Together with these measurements the Efficency can be calculated.

@author: conor
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
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, title, size):
        
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1])
        
        # widgets
        self.menu = Menu(self)
        
        # run
        self.mainloop()
        
class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        # GUI variables
        self.voltage = "0"
        self.cell_area = 'Leaf'
        self.cell = 1
        self.current = 25
        self.data_points = 25
        self.hours = 0
        self.minutes = 0
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def voltage_callback(choice):
            print("voltage:", choice)
            self.voltage = choice
        
        def cell_area_callback(choice):
            print("cell type:", choice)
            self.cell_area = choice
        
        def cell_callback(value):
            print("number of cells:", value)
            self.cell = value
            
        def compliance_current_callback(value):
            print("compliance current:", value)
            self.current = value
            
        def data_points_callback(value):
            print("data points:", value)
            self.data_points = value
            
        def hours_callback(choice):
            print("hours:", choice)
            self.hours = choice
        
        def minutes_callback(choice):
            print("minutes:", choice)
            self.minutes = choice
    
        def start_button_event():
            Measurement.loop(self)
        
        # create widgets
        menu_button1 = ctk.CTkButton(self, text = 'Start Measurement Session', command = start_button_event)
        
        optionmenu_voltage = ctk.StringVar(value = "0")
        optionmenu_voltage = ctk.CTkOptionMenu(self,values=["0", "5", "10", "15", "20",
                                                       "25", "30", "35", "40", "45",
                                                       "50", "55", "60"],
                                         command=voltage_callback,
                                         variable=optionmenu_voltage)
        
        segmented_frame_1 = ctk.CTkFrame(self)
        cell_var = ctk.IntVar(value = 1)
        cell_button = ctk.CTkSegmentedButton(segmented_frame_1, values=[1, 2, 3],
                                                         command=cell_callback,
                                                         variable=cell_var)
        
        optionmenu_cell_area = ctk.StringVar(value = "Leaf")
        cell_area_button = ctk.CTkOptionMenu(self, values=['Leaf', 'Diamond'],
                                                         command=cell_area_callback,
                                                         variable=optionmenu_cell_area)
        
        segmented_frame_2 = ctk.CTkFrame(self)
        compliance_current_var = ctk.IntVar(value = 25)
        compliance_current_button = ctk.CTkSegmentedButton(segmented_frame_2, values=[25, 250, 500, 1000],
                                                         command=compliance_current_callback,
                                                         variable=compliance_current_var)
        segmented_frame_3 = ctk.CTkFrame(self)
        data_points_var = ctk.IntVar(value = 25)
        data_points_button = ctk.CTkSegmentedButton(segmented_frame_3, values=[25, 50, 100, 150, 300],
                                                         command=data_points_callback,
                                                         variable=data_points_var)
        optionmenu_hours = ctk.StringVar(value = "0")
        optionmenu_hr = ctk.CTkOptionMenu(self,values=["0", "1", "2", "3", "4",
                                                       "5", "6", "7", "8", "9",
                                                       "10", "11", "12"],
                                         command=hours_callback,
                                         variable=optionmenu_hours)
        
        optionmenu_minutes = ctk.StringVar(value = "0")
        optionmenu_mi = ctk.CTkOptionMenu(self,values=["0", "5", "10", "15",
                                                       "20", "25", "30", "35",
                                                       "40", "45", "50", "55"],
                                         command=minutes_callback,
                                         variable=optionmenu_minutes)
        
        # create labels
        title = ctk.CTkLabel(self, text = "OPV AMP", font = ("Helvetica", 30), anchor = "center", fg_color = "transparent")
        label_cells = ctk.CTkLabel(self, text = "Number of Cells")
        label_cell_area = ctk.CTkLabel(self, text = "Cell Type")
        label_voltage = ctk.CTkLabel(self, text = "Voltage [V]")
        label_current = ctk.CTkLabel(self, text = "Current Compliance [mA]")
        label_data_points = ctk.CTkLabel(self, text = "Data Points")
        label_measurement_time = ctk.CTkLabel(self, text = "Measurement Time")
        label_hours = ctk.CTkLabel(self, text = "Hours")
        label_minutes = ctk.CTkLabel(self, text = "Minutes")
         # create the grid
        self.columnconfigure((4), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight = 1, uniform = 'a')
        
        # place the widgets and labels
        title.grid(row = 0, column = 1, columnspan = 6, sticky = "nsew")
        label_cells.grid(row = 1, column = 1, padx = 20, pady = 20)
        segmented_frame_1.grid(row = 1, column = 3, sticky = 'nswe', columnspan = 2)
        cell_button.pack(side = 'right', expand = True, pady = 20)
        label_cell_area.grid(row = 2, column = 1, padx = 20, pady = 20)
        cell_area_button.grid(row = 2, column = 3, columnspan = 3)
        label_voltage.grid(row = 3, column = 1, padx = 20, pady = 20)
        optionmenu_voltage.grid(row = 3, column = 3, columnspan = 3)
        label_current.grid(row = 4, column = 1, padx = 20, pady = 20)
        segmented_frame_2.grid(row = 4, column = 3, sticky = 'nsew', columnspan = 2)
        compliance_current_button.pack(expand = False, pady = 20)
        label_data_points.grid(row = 5, column = 1, padx = 20, pady = 20)
        segmented_frame_3.grid(row = 5, column = 3, sticky = 'nswe', columnspan = 2)
        data_points_button.pack(expand = False, pady = 20)
        label_measurement_time.grid(row = 6, column = 1, rowspan = 2, padx = 20, pady = 20)
        label_hours.grid(row = 6, column = 2, padx = 20, pady = 20)
        optionmenu_hr.grid(row = 6, column = 3, columnspan = 2)
        label_minutes.grid(row = 7, column = 2, padx = 20, pady = 20)
        optionmenu_mi.grid(row = 7, column = 3, columnspan = 2)
        
        menu_button1.grid(row = 8, column = 0, stick = 'nsew', columnspan = 6)
        
        
class Measurement(): 
    def __init__(self):
        super().__init__()
           
    def loop(self):
        # Instruments
        adapter = PrologixAdapter('ASRL3::INSTR')
        sourcemeter = Keithley2400(adapter.gpib(24))  # at GPIB address 24
        switchsystem = Keithley2750(adapter.gpib(17))  # at GPIB address 17
        
        # Sourcemeter Constants
        averages = 10
        measure_nplc = 0.1  # Number of power line cycles
        max_voltage = 0 # in Volts
        
        # Efficiency Calculation Constants
        ref_power = 104.749 # mV / W/m²
        stc_power = 1000 # W/m²

        # Cell Area
        cell_area = self.cell_area
        if cell_area == 'Diamond':
            cell_area = 0.1122
        else:
            cell_area = 0.075

        # Temperature Calculation Constants
        RES_0 = 1000
        TEMP_A = 0.0039083
        TEMP_B = -0.0000005775
        
        # Switch System Setup
        switchsystem.write(':open all')
        switchsystem.write('*RST')
        
        # Number of Cells Parameters
        cell_1 = 'cell_1' # channels 1 & 2 - pins 13a, 14a, 15a and 16a
        cell_2 = 'cell_2' # channels 3 & 4 - pins 6a, 7a, 12a and 11a
        cell_3 = 'cell_3' # channels 5 & 6 - pins 2a, 3a, 4a and 5a
        cell = self.cell
        
        if cell == 1:
            test_ch = {cell_1 : '1!1, 1!2'}
        elif cell == 2:
            test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4'}
        else:
            test_ch = {cell_1 : '1!1, 1!2', cell_2 : '1!3, 1!4', cell_3 : '1!5, 1!6'}
        
        ref_cell = '1!7, 1!8' # channels 7 & 8 - pins 21a, 18a, 8a and 10a
        temp_sensor = '1!9, 1!10' # channels 9 & 10 - pins 4b, 5b, 12b and 11b
        
        # Voltage Parameters
        voltage_range = int(self.voltage)
        min_voltage = -(int(self.voltage))
        
        # Compliance Current Parameters
        compliance_current = self.current / 1000
        current_range = compliance_current
        
        # Data Points Parameters
        data_points = self.data_points
        
        # Time Parameters
        hours = int(self.hours)
        minutes = int(self.minutes)
        timeout = (hours * 3600) + (minutes * 60) # seconds
        
        print('Script Parameters:\nChannels:',test_ch,'\nVoltage Range:',
              voltage_range,'\nMin Voltage',min_voltage, '\nCompliance Current:',
              compliance_current,'\nCurrent Range:', current_range, '\nData Points:',
              data_points, '\nMeasurement Time:',hours,'Hours,',minutes,'Minutes',
              '\nTotal',timeout,'Seconds')
        
        # Create Arrays for Results
        voltages = np.linspace(max_voltage, min_voltage, num=data_points)
        currents = np.zeros_like(voltages)
        current_stds = np.zeros_like(voltages)

        # Path to save results
        path = os.getcwd() # needs updating to properly find where the code is situated and output the results there
        def run():
            # Sets the initial time value when the program is started
            timeout_start = time.time()
            print('starting measurement cycle...')
            # Create an empty dataframe to collect all results outside the loop
            final = pd.DataFrame()
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
                        # Voltage at MPP
                        mppv = data.iloc[data['Power (W)'].argmax()]['Voltage (V)']
                        # Current at MPP
                        mppi = data.iloc[data['Power (W)'].argmax()]['Current (A)']
                        # Theoretical MPP per square metre
                        mppsqm = mpp/cell_area
                        
                        # Calculate the Fill Factor
                        ff = mpp/(isc*voc)
                
                        # Calculate the reference solar cell irradiation
                        irradiation = (ref_sig*1000 / ref_power)*stc_power # in W/m²
                
                        # Calculate the efficiency of the cell
                        eff = 100 * (mpp / (cell_area * irradiation)) # in %
                        
                        # Calculate the temperature from the resistance 
                        temp = (-TEMP_A + math.sqrt((TEMP_A**2)-(4*TEMP_B*(1-(temp_res/RES_0)))))/(2*TEMP_B) # in °C
                        
                        # Create a dictionary for the results
                        results = {"Timestamp" : [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                                "Cell" : [ch],
                                "Isc" : [isc],
                                "Voc" : [voc],
                                "MPP" : [mpp],
                                "MPPv" : mppv,
                                "MPPi" : mppi,
                                "MPPsqm" : mppsqm,
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
            final.to_csv(os.path.join(path, 'opv_amp_'+ datetime.now().strftime("%Y-%m-%d_%H-%M")+'.csv')) # this needs to be an iterable name that doesn't always overwrite previous results

            print('results successfully saved\nfile path:',
                  os.path.join(path, 'opv_amp_'+ datetime.now().strftime("%Y-%m-%d_%H-%M")+'.csv'))
            # Reset switch system and sourcemeter
            switchsystem.write(':open all')
            switchsystem.write('*RST')
            sourcemeter.shutdown()

            print('all instruments successfully shutdown \nmeasurement session ended')

        run()
        
App('OPV AMP', (800,800))