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
        self.hours = 0
        self.minutes = 0
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def hours_callback(choice):
            print("hours:", choice)
            self.hours = choice
        
        def minutes_callback(choice):
            print("minutes:", choice)
            self.minutes = choice
        
        def button_event():
            Time.timeout(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Button 1', command = button_event)
        
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
        self.columnconfigure((0), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 0, column = 0, stick = 'nswe', columnspan = 2)
        optionmenu_hr.grid(row = 1, column = 0, columnspan = 2)
        optionmenu_mi.grid(row = 1, column = 1)
        
class Time():
    def __init__(self):
        super().__init__()
    
    def timeout(self):
        hours = int(self.hours)
        minutes = int(self.minutes)
        print('measurements will run for',hours,'hour(s) and',minutes,'minutes')
        timeout = (hours * 3600) + (minutes * 60) # seconds
        print(timeout)
        
App('class based app', (600,600))