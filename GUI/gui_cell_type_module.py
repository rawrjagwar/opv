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
        self.cell_area = 'Leaf'
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 0.7, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def cell_callback(value):
            print("segmented button clicked:", value)
            self.cell_area = value
        
        def button_event():
            Cell.number(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Button 1', command = button_event)
        
        optionmenu_cell_area = ctk.StringVar(value = "Leaf")
        cell_area_button = ctk.CTkOptionMenu(self, values=['Leaf', 'Diamond'],
                                                         command=cell_callback,
                                                         variable=optionmenu_cell_area)
        
        # create the grid
        self.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 0, column = 0, stick = 'nswe', columnspan = 2)
        cell_area_button.grid(row = 1)

class Cell():
    def __init__(self):
        super().__init__()
    
    def number(self):
        # Switch System Variables
        cell_area = self.cell_area
        if cell_area == 'Diamond':
            cell_area = 0.1122
        else:
            cell_area = 0.075
        print(cell_area)
        
App('class based app', (600,600))