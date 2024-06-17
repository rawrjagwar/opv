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
        self.data_points = 25
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 0.7, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def data_points_callback(value):
            print("segmented button clicked:", value)
            self.data_points = value
        
        def button_event():
            Cell.number(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Button 1', command = button_event)
        
        segmented_frame = ctk.CTkFrame(self)
        data_points_var = ctk.IntVar(value = 25)
        data_points_button = ctk.CTkSegmentedButton(segmented_frame, values=[10, 25, 50],
                                                         command=data_points_callback,
                                                         variable=data_points_var)
        
        # create the grid
        self.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 0, column = 0, stick = 'nswe', columnspan = 2)
        segmented_frame.grid(row = 1, column = 0, stick = 'nswe', columnspan = 2)
        data_points_button.pack(side = 'left', expand = True)

class Cell():
    def __init__(self):
        super().__init__()
    
    def number(self):
        data_points = self.data_points
        print(data_points)
        
App('class based app', (600,600))