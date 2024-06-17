# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:57:03 2024

@author: conor
"""
import customtkinter
import sys,os
sys.path.append(os.getcwd())
from test_loop_print import loop

app = customtkinter.CTk()
app.title("my app")
app.geometry("600x500")


def optionmenu_callback(choice):
    VAR_A = []
    print("optionmenu dropdown clicked:", choice)
    VAR_A = int(optionmenu.get())

optionmenu_var = customtkinter.StringVar(value="2")
optionmenu = customtkinter.CTkOptionMenu(app,values=["1", "2","3"],
                                         command=optionmenu_callback,
                                         variable=optionmenu_var)

def button_callback():
    VAR_A = int(optionmenu.get())
    print(VAR_A)
    
    
button = customtkinter.CTkButton(app, text="print", command=button_callback)

def button_square():
    VAR_A = int(optionmenu.get())
    VAR_A[0] += 2
    
button_2 = customtkinter.CTkButton(app, text="add 2", command=button_square)

def button_script():
    loop()

button_3 = customtkinter.CTkButton(app, text="loop", command=button_script)

# Populating window

optionmenu.grid(row=0, column=0, padx=20,pady=20)

button.grid(row=2, column=0, padx=20, pady=20)

button_2.grid(row = 4, column=0, padx=20, pady=20)

button_3.grid(row = 6, column=0, padx=20, pady=20)

app.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app.mainloop()