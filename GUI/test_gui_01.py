# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:57:03 2024

@author: conor
"""
import customtkinter
import sys,os
sys.path.append(os.getcwd())
from test_loop_print import loop

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

app = App()

optionmenu_var = customtkinter.StringVar(value="option 2")
optionmenu = customtkinter.CTkOptionMenu(app,values=["option 1", "option 2"],
                                         command=optionmenu_callback,
                                         variable=optionmenu_var)

optionmenu.grid(row=2, column=0, padx=20, pady=20)



if __name__=="__main__":
    app.mainloop()