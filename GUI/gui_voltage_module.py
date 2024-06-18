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
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def voltage_callback(choice):
            print("voltage:", choice)
            self.voltage = choice
        
        def button_event():
            Voltage.voltage(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Button 1', command = button_event)
        
        optionmenu_voltage = ctk.StringVar(value = "0")
        optionmenu_voltage = ctk.CTkOptionMenu(self,values=["0", "5", "10", "15", "20",
                                                       "25", "30", "35", "40", "45",
                                                       "50", "55", "60"],
                                         command=voltage_callback,
                                         variable=optionmenu_voltage)
        
         # create the grid
        self.columnconfigure((0), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 0, column = 0, stick = 'nswe', columnspan = 2)
        optionmenu_voltage.grid(row = 1, column = 0, columnspan = 2)

        
class Voltage():
    def __init__(self):
        super().__init__()
    
    def voltage(self):
        voltage_range = int(self.voltage)
        min_voltage = -(int(self.voltage))
        print(voltage_range,"V")
        print(min_voltage,"V")
        
App('class based app', (600,600))