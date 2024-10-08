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
        self.current = 25
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 0.7, relheight = 1)
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        def compliance_current_callback(value):
            print("segmented button clicked:", value)
            self.current = value
        
        def button_event():
            Compliance.current(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Button 1', command = button_event)
        
        segmented_frame_2 = ctk.CTkFrame(self)
        compliance_current_var = ctk.IntVar(value = 25)
        compliance_current_button = ctk.CTkSegmentedButton(segmented_frame_2, values=[25, 250, 500, 1000],
                                                         command=compliance_current_callback,
                                                         variable=compliance_current_var)
        
        # create the grid
        self.columnconfigure((0,1,2), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 0, column = 0, stick = 'nswe', columnspan = 2)
        segmented_frame_2.grid(row = 1, column = 0, stick = 'nswe', columnspan = 2)
        compliance_current_button.pack(side = 'left', expand = True)

class Compliance():
    def __init__(self):
        super().__init__()
    
    def current(self):
        compliance_current = self.current / 1000
        current_range = compliance_current
        print('compliance current:',compliance_current)
        print('current range:',current_range)
        
App('class based app', (600,600))