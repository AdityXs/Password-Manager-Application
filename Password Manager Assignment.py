from tkinter import *
import customtkinter

root = customtkinter.CTk()



root.title('Password Manager')
root.geometry('900x700')


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme('blue')


instruction_label = customtkinter.CTkLabel(root, text = "Please create your Master Password")
instruction_label.pack()


#Code for instruction inside entry field 
def entry_focus_in(event):
    if entry_1.get() == "Choose Password":
        entry_1.delete(0, 'end')
        entry_1.config(fg="gray") #what is this??


def entry_focus_out(event):
    if entry_1.get() == "":
        entry_1.insert(0, "Choose Password")
        entry_1.config(fg='gray')

def entry_focus_in2(event):
    if entry_2.get() == "Confirm Password":
        entry_2.delete(0, 'end')
        entry_2.config(fg="gray") #what is this??


def entry_focus_out2(event):
    if entry_2.get() == "":
        entry_2.insert(0, "Confirm Password")
        entry_2.config(fg='gray')


#Entry Fields

entry_1 = customtkinter.CTkEntry(root, width=170, height=20)
entry_1.pack(pady=30)
entry_1.insert(0,"Choose Password")
entry_1.bind("<FocusIn>", entry_focus_in)
entry_1.bind("<FocusOut>", entry_focus_out)


entry_2 = customtkinter.CTkEntry(root, width=170, height=20)
entry_2.pack(pady=30)
entry_2.insert(0,"Confirm Password")
entry_2.bind("<FocusIn>", entry_focus_in2)
entry_2.bind("<FocusOut>", entry_focus_out2)


checkbutton = customtkinter.CTkButton(root, text = "Check")
checkbutton.pack(pady = 30)
root.mainloop()