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
        self.cell = 1
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 0.7, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def cell_callback(value):
            print("segmented button clicked:", value)
            self.cell = value
        
        def button_event():
            Cell.number(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Button 1', command = button_event)
        
        segmented_frame_1 = ctk.CTkFrame(self)
        cell_var = ctk.IntVar(value = 1)
        cell_button = ctk.CTkSegmentedButton(segmented_frame_1, values=[1, 2, 3],
                                                         command=cell_callback,
                                                         variable=cell_var)
        
        # create the grid
        self.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 0, column = 0, stick = 'nswe', columnspan = 2)
        segmented_frame_1.grid(row = 1, column = 0, stick = 'nswe', columnspan = 2)
        cell_button.pack(side = 'left', expand = True)

class Cell():
    def __init__(self):
        super().__init__()
    
    def number(self):
        # Switch System Variables
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
        print(test_ch)
        
App('class based app', (600,600))