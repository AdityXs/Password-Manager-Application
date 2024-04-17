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
        entry_1.configure(fg_color="gray") #what is this??


def entry_focus_out(event):
    if entry_1.get() == "":
        entry_1.insert(0, "Choose Password")
        entry_1.configure(fg_color='gray')

def entry_focus_in2(event):
    if entry_2.get() == "Confirm Password":
        entry_2.delete(0, 'end')
        entry_2.configure(fg_color="gray") #what is this??


def entry_focus_out2(event):
    if entry_2.get() == "":
        entry_2.insert(0, "Confirm Password")
        entry_2.configure(fg_color='gray')

#Password Validator... Need to work on this later but core mechanic works for now
def check_passwords():
    password1 = entry_1.get()
    password2 = entry_2.get()
    if password1 == password2:
        print("Passwords match!")
    else:
        print("Passwords do not match!")

def toggle_password_visibility(entry):
    if entry.cget('show') == '':
        entry.configure(show='*')
    else:
        entry.configure(show='')

#Entry Fields

entry_1 = customtkinter.CTkEntry(root, width=170, height=20)
entry_1.pack(pady=30)
entry_1.insert(0,"Choose Password")
entry_1.bind("<FocusIn>", entry_focus_in)
entry_1.bind("<FocusOut>", entry_focus_out)

#Hide Password Button
eye_button_1 = customtkinter.CTkButton(root, text="Show/Hide", command=lambda: toggle_password_visibility(entry_1))
eye_button_1.pack(pady=10)

#Entry Fields 2

entry_2 = customtkinter.CTkEntry(root, width=170, height=20)
entry_2.pack(pady=30)
entry_2.insert(0,"Confirm Password")
entry_2.bind("<FocusIn>", entry_focus_in2)
entry_2.bind("<FocusOut>", entry_focus_out2)

#Hide Password button
eye_button_2 = customtkinter.CTkButton(root, text="Show/Hide", command=lambda: toggle_password_visibility(entry_2))
eye_button_2.pack(pady=10)

#Have to make the validation message appear on window 
checkbutton = customtkinter.CTkButton(root, text="Confirm", command=check_passwords)
checkbutton.pack(pady = 30)

root.mainloop()