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
        self.var_1 = 20
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        self.create_widgets()
        
    def create_widgets(self):
        
        def segmented_button_callback(value):
            print("segmented button clicked:", value)
            self.var_1 = value
        
        def button_event():
            Loop.action(self)
            
        menu_button1 = ctk.CTkButton(self, text = 'Start Measurements', command = button_event)
        
        segmented_frame = ctk.CTkFrame(self)
        segmented_button_var = ctk.IntVar(value = 20)
        segmented_button = ctk.CTkSegmentedButton(segmented_frame, width = 10, height = 50, values=[20, 50, 100],
                                                         command=segmented_button_callback,
                                                         variable=segmented_button_var)
        button_label = ctk.CTkLabel(self, text = "Compliance Current (mA)")
        
        progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        
        # create the grid
        self.columnconfigure((0,1,2,3), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2), weight = 1, uniform = 'a')
        
        # place the widgets
        menu_button1.grid(row = 3, column = 1, columnspan = 2, pady = 50)
        segmented_frame.grid(row = 1, column = 2, columnspan = 2)
        segmented_button.pack(expand = True)
        button_label.grid(row=1, column=0)

class Loop():
    def __init__(self):
        super().__init__()
    
    def action(self):
        a = int(self.var_1)
        a *= 2
        print(a)
        
        
App('OPV AMP', (800,600))