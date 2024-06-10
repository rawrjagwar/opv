# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:21:21 2024

@author: coray
"""

import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("my app")
app.geometry("400x150")

button = customtkinter.CTkButton(app, text="my button", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

def checkbox_event():
    print("checkbox toggled, current value:", check_var.get())

check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(app, text="CTkCheckBox", command=checkbox_event,
                                     variable=check_var, onvalue="on", offvalue="off")

checkbox.grid(row=1, column=1, padx=40, pady=40)

app.grid_columnconfigure(0, weight=1)

app.mainloop()