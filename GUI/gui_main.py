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
            Voltage.voltage(self) # all variables need to be here and then referenced from the main loop class
            
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
        data_points_button = ctk.CTkSegmentedButton(segmented_frame_3, values=[10, 25, 50],
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
        
         # create the grid
        self.columnconfigure((4), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4,5,6,7), weight = 1, uniform = 'a')
        
        # place the widgets
        segmented_frame_1.grid(row = 1, column = 4)
        cell_button.pack(side = 'right', expand = False)
        
        optionmenu_voltage.grid(row = 2, column = 4, columnspan = 2)
        
        segmented_frame_2.grid(row = 3, column = 4, stick = 'nswe', columnspan = 2)
        compliance_current_button.pack(expand = False)
        
        segmented_frame_3.grid(row = 4, column = 3, stick = 'nswe', columnspan = 2)
        data_points_button.pack(expand = False)
        
        optionmenu_hr.grid(row = 5, column = 3, columnspan = 2)
        optionmenu_mi.grid(row = 6, column = 3, columnspan = 2)
        
        menu_button1.grid(row = 7, column = 3, stick = 'nswe', columnspan = 3)
        
        
class Voltage(): # this is where the main loop class will be
    def __init__(self):
        super().__init__()
    
    def voltage(self):
        voltage_range = int(self.voltage)
        min_voltage = -(int(self.voltage))
        print(voltage_range,"V")
        print(min_voltage,"V")
        
App('class based app', (600,600))