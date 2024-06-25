# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:35:25 2024

@author: conor
"""

import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, title, size):
        
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        
        # widgets
        self.menu = Menu(self)
        
        # run
        self.mainloop()
        
class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        # GUI variables
        self.voltage = "0"
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
        
        def cell_callback(value):
            print("segmented button clicked:", value)
            self.cell = value
            
        def compliance_current_callback(value):
            print("segmented button clicked:", value)
            self.current = value
            
        def data_points_callback(value):
            print("segmented button clicked:", value)
            self.data_points = value
            
        def hours_callback(choice):
            print("hours:", choice)
            self.hours = choice
        
        def minutes_callback(choice):
            print("minutes:", choice)
            self.minutes = choice
    
        def start_button_event():
            Measurement.parameters(self) # all variables need to be here and then referenced from the main loop class
        
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
        segmented_frame_2 = ctk.CTkFrame(self)
        compliance_current_var = ctk.IntVar(value = 25)
        compliance_current_button = ctk.CTkSegmentedButton(segmented_frame_2, values=[25, 250, 500, 1000],
                                                         command=compliance_current_callback,
                                                         variable=compliance_current_var)
        segmented_frame_3 = ctk.CTkFrame(self)
        data_points_var = ctk.IntVar(value = 25)
        data_points_button = ctk.CTkSegmentedButton(segmented_frame_3, values=[10, 25, 50, 100],
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
        label_voltage = ctk.CTkLabel(self, text = "Voltage [V]")
        label_current = ctk.CTkLabel(self, text = "Current Compliance [mA]")
        label_data_points = ctk.CTkLabel(self, text = "Data Points")
        label_measurement_time = ctk.CTkLabel(self, text = "Measurement Time")
        label_hours = ctk.CTkLabel(self, text = "Hours")
        label_minutes = ctk.CTkLabel(self, text = "Minutes")
         # create the grid
        self.columnconfigure((4), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4,5,6,7), weight = 1, uniform = 'a')
        
        # place the widgets and labels
        title.grid(row = 0, column = 1, columnspan = 6, sticky = "nsew")
        label_cells.grid(row = 1, column = 1, padx = 20, pady = 20)
        segmented_frame_1.grid(row = 1, column = 3, sticky = 'nswe', columnspan = 2)
        cell_button.pack(side = 'right', expand = True, pady = 20)
        label_voltage.grid(row = 2, column = 1, padx = 20, pady = 20)
        optionmenu_voltage.grid(row = 2, column = 3, columnspan = 3)
        label_current.grid(row = 3, column = 1, padx = 20, pady = 20)
        segmented_frame_2.grid(row = 3, column = 3, sticky = 'nsew', columnspan = 2)
        compliance_current_button.pack(expand = False, pady = 20)
        label_data_points.grid(row = 4, column = 1, padx = 20, pady = 20)
        segmented_frame_3.grid(row = 4, column = 3, sticky = 'nswe', columnspan = 2)
        data_points_button.pack(expand = False, pady = 20)
        label_measurement_time.grid(row = 5, column = 1, rowspan = 2, padx = 20, pady = 20)
        label_hours.grid(row = 5, column = 2, padx = 20, pady = 20)
        optionmenu_hr.grid(row = 5, column = 3, columnspan = 2)
        label_minutes.grid(row = 6, column = 2, padx = 20, pady = 20)
        optionmenu_mi.grid(row = 6, column = 3, columnspan = 2)
        
        menu_button1.grid(row = 7, column = 0, stick = 'nsew', columnspan = 6)
        
        
class Measurement(): # this is where the main loop class will be
    def __init__(self):
        super().__init__()
            
    def parameters(self):
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
        
        def time(self):
            timeout
App('OPV AMP', (600,600))