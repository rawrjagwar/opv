# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:21:21 2024

@author: coray
"""

import tkinter
import customtkinter



def button_callback():
    variable = [int(optionmenu.get())]
    square = variable[0]**2
    print(square)
    

app = customtkinter.CTk()
app.title("my app")
app.geometry("400x500")

button = customtkinter.CTkButton(app, text="square me", command=button_callback)
#button.grid(row=2, column=0, padx=20, pady=20)

def checkbox_event():
    print("checkbox toggled, current value:", check_var.get())

check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(app, text="CTkCheckBox", command=checkbox_event,
                                     variable=check_var, onvalue="on", offvalue="off")

#checkbox.grid(row=1, column=1, padx=40, pady=40)

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)
    variable = [int(optionmenu.get())]
    print(variable)
    min_voltage = -(variable[0])
    print(min_voltage)

optionmenu_var = customtkinter.StringVar(value="2")
optionmenu = customtkinter.CTkOptionMenu(app,values=["1", "2","3"],
                                         command=optionmenu_callback,
                                         variable=optionmenu_var)

#optionmenu.grid(row=0, column=0, padx=20,pady=20)

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox = customtkinter.CTkComboBox(app, values=["option 1", "option 2"],
                                     command=combobox_callback)
combobox.set("option 2")

#combobox.grid(row=10)

def segmented_button_callback(value):
    print("segmented button clicked:", value)

segemented_button = customtkinter.CTkSegmentedButton(app, values=["One", "Two", "Three"],
                                                     command=segmented_button_callback)
segemented_button.set("One")

#segemented_button.grid(row=1, column=0)

def switch_event():
    print("switch toggled, current value:", switch_var.get())

switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(app, text="Beeps", command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off")

#switch.grid(row=2,column=0)

progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal", mode = 'indeterminate')

progressbar.grid(row = 2, columnspan = 20, pady = 20)

progressbar.start()

app.grid_columnconfigure(0, weight=1)

app.mainloop()