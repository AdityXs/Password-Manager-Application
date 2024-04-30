from tkinter import *
import customtkinter
import random 
import string
import pyperclip
from tkinter import messagebox
from PIL import ImageTk, Image
import os

#Loading Images
file_path = os.path.dirname(os.path.realpath(__file__))
eye_image = customtkinter.CTkImage(Image.open(file_path +
                                              "/redness.png"), size =(35, 35))

logo_image = customtkinter.CTkImage(Image.open(file_path +
                                              "/image.png"), size =(35, 35))

copy_image = customtkinter.CTkImage(Image.open(file_path +
                                              "/copy.png"), size =(35, 35))


MASTER_PASSWORD_FILE = "master_password.txt"
LOGIN_INFO_FILE = "login_info.txt"



def create_main_window():
    root = customtkinter.CTk()

    root.title('Create Password')
    root.geometry('900x700')

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme('blue')

    instruction_label = customtkinter.CTkLabel(root, text="Please create your Master Password")
    instruction_label.pack()

    def check_passwords():
        password1 = entry_1.get()
        password2 = entry_2.get()
        if len(password1) < 8 or len(password2) < 8:
            feedback_label.configure(text="Please choose a longer password", fg_color="red", corner_radius=8)
        elif password1 == password2:
            feedback_label.configure(text="Accepted", fg_color="green", corner_radius=8)
            # Save master password
            save_master_password(password1)
            # Once passwords are accepted, open the blank window
            root.destroy()
            main_application_window()
        else:
            feedback_label.configure(text="Passwords Do Not Match", fg_color="red", corner_radius=8)

    def toggle_password_visibility(entry):
        if entry.cget('show') == '':
            entry.configure(show='•')
        else:
            entry.configure(show='')

    entry_1_frame = Frame(root, bg=root.cget('bg')) #bg=root.cget('bg') <-- add this later to make the background transparent 
    entry_1_frame.pack(pady=30)

    choose_password_label = customtkinter.CTkLabel(entry_1_frame, text="Choose Password:")
    choose_password_label.pack(side=LEFT, padx=(0, 10))

    entry_1 = customtkinter.CTkEntry(entry_1_frame, width=150, height=20, show='•')  # Initially hide the password
    entry_1.pack(side=LEFT)

    toggle_button_1 = customtkinter.CTkButton(entry_1_frame, image = eye_image, text="", command=lambda: toggle_password_visibility(entry_1), fg_color='#E97451')
    toggle_button_1.pack(side=LEFT)

    entry_2_frame = Frame(root, bg=root.cget('bg')) #bg=root.cget('bg') <-- add this later to make the background transparent
    entry_2_frame.pack(pady=30)

    confirm_password_label = customtkinter.CTkLabel(entry_2_frame, text="Confirm Password:")
    confirm_password_label.pack(side=LEFT, padx=(0, 10))

    entry_2 = customtkinter.CTkEntry(entry_2_frame, width=150, height=20, show='•')  # Initially hide the password
    entry_2.pack(side=LEFT)

    toggle_button_2 = customtkinter.CTkButton(entry_2_frame, image = eye_image, text="", command=lambda: toggle_password_visibility(entry_2), fg_color='#E97451')
    toggle_button_2.pack(side=LEFT)

    checkbutton = customtkinter.CTkButton(root, text="Check", command=check_passwords, fg_color='#E97451')
    checkbutton.pack(pady=10)

    feedback_label = customtkinter.CTkLabel(root, text="")
    feedback_label.pack(pady=5)

    root.mainloop()


def main_application_window():
    # Loading Images
    file_path = os.path.dirname(os.path.realpath(__file__))
    eye_image = customtkinter.CTkImage(Image.open(file_path + "/redness.png"), size=(35, 35))
    logo_image = customtkinter.CTkImage(Image.open(file_path + "/image.png"), size=(140, 140))
    copy_image = customtkinter.CTkImage(Image.open(file_path + "/copy.png"), size=(35, 35))

    password_generator_added = False
    login_fields_added = False  

    def generate_password():
        password_length = int(length_entry.get())

        password_chars = string.ascii_letters
        if include_numbers.get():
            password_chars += string.digits
        if include_special_chars.get():
            password_chars += string.punctuation

        password = ''.join(random.choice(password_chars) for i in range(password_length))

        password_label.configure(text=password)

    def copy_password():
        password = password_label.cget('text')
        pyperclip.copy(password)
        messagebox.showinfo('Password Copied', 'The password has been copied to the clipboard')

    def generate_password_gui():
        nonlocal password_generator_added

        if not password_generator_added:
            global length_entry, include_numbers, include_special_chars, password_label

            password_gen_frame = customtkinter.CTkFrame(main_window)  
            password_gen_frame.place(relx=0.5, rely=0.5, anchor='center')
            

            length_label = customtkinter.CTkLabel(password_gen_frame, text="Password length:", text_color='white', font=('Arial', 14, 'bold'))
            length_label.grid(row=0, column=0, pady = 10)

            length_entry = customtkinter.CTkEntry(password_gen_frame)
            length_entry.grid(row=1, column=0, pady=10)

            include_numbers = BooleanVar()
            number_check = customtkinter.CTkCheckBox(password_gen_frame, text="Include numbers", text_color='white',
                                                     variable=include_numbers, font=('Arial', 14, 'bold'))
            number_check.grid(row=2, column=0, pady=10)

            include_special_chars = BooleanVar()
            special_check = customtkinter.CTkCheckBox(password_gen_frame, text="Include special characters",
                                                      text_color='white', font=('Arial', 14, 'bold'), variable=include_special_chars)
            special_check.grid(row=3, column=0, padx =5, pady=10)

            generate_button = customtkinter.CTkButton(password_gen_frame, text="Generate Password",
                                                      command=generate_password, fg_color='#E97451', font=('Arial', 14, 'bold'))
            generate_button.grid(row=4, column=0, pady=10)

            password_label = customtkinter.CTkLabel(password_gen_frame, text="", font=('Arial', 14, 'bold'))
            password_label.grid(row=5, column=0, pady=10)

            copy_button = customtkinter.CTkButton(password_gen_frame, image=copy_image, compound='right',
                                                  text="Copy Password", command=copy_password, fg_color='#E97451', font=('Arial', 14, 'bold'))
            copy_button.grid(row=6, column=0, pady=10)

            password_generator_added = True

    def add_login_fields():
        nonlocal login_fields_added
        if not login_fields_added:


            # Create the actual frame inside the border frame
            login_fields_frame = customtkinter.CTkFrame(main_window, width=450, height=80)  
            login_fields_frame.place(relx=0.27, rely=0.435, anchor='center')
        
            site_label = customtkinter.CTkLabel(login_fields_frame, text="Site:", text_color='white', font=('Arial', 14, 'bold'))
            site_label.grid(row=0, column=0)

            site_entry = customtkinter.CTkEntry(login_fields_frame, width = 250)
            site_entry.grid(row=0, column=1, padx=10, pady=10)

            username_label = customtkinter.CTkLabel(login_fields_frame, text="Username/email:", text_color='white', font=('Arial', 14, 'bold'))
            username_label.grid(row=1, column=0, padx=10)

            username_entry = customtkinter.CTkEntry(login_fields_frame, width = 250)
            username_entry.grid(row=1, column=1, padx=10, pady=5)

            password_label = customtkinter.CTkLabel(login_fields_frame, text="Password:", text_color='white', font=('Arial', 14, 'bold'))
            password_label.grid(row=2, column=0)

            password_entry = customtkinter.CTkEntry(login_fields_frame, show='•', width = 250)
            password_entry.grid(row=2, column=1, padx=10, pady=5)

            def toggle_password_visibility():
                if password_entry.cget('show') == '':
                    password_entry.configure(show='•')
                else:
                    password_entry.configure(show='')

            def clear_entry_fields():
                site_entry.delete(0, 'end')
                username_entry.delete(0, 'end')
                password_entry.delete(0, 'end')

            show_hide_button = customtkinter.CTkButton(login_fields_frame, image=eye_image, text="",
                                                        command=toggle_password_visibility, fg_color='#E97451')
            show_hide_button.grid(row=2, column=2, padx=10, pady=5)

            def save_login_info():
                site = site_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                if site and username and password:
                    if not is_login_saved(site, username, password):
                        save_login(site, username, password)  
                        feedback_label.configure(text="Login information saved", fg_color="green", corner_radius=8)

                    else:
                        feedback_label.configure(text="Login information already saved", fg_color="red",
                                                 corner_radius=8)
                else:
                    feedback_label.configure(text="Please fill in all fields", fg_color="red", corner_radius=8)

            def is_login_saved(site, username, password):
                try:
                    with open(LOGIN_INFO_FILE, "r") as file:
                        for line in file:
                            if f"Site: {site}, Username/email: {username}, Password: {password}" in line:
                                return True
                except FileNotFoundError:
                    with open(LOGIN_INFO_FILE, "w"):
                        pass  
                return False

            save_button = customtkinter.CTkButton(login_fields_frame, text="Save", font=('Arial', 14, 'bold'), command=save_login_info,
                                                  fg_color='#E97451')
            save_button.place(anchor = 'c', relx =0.48, rely = .75)

            feedback_label = customtkinter.CTkLabel(login_fields_frame, text="", font=('Arial', 14, 'bold'))
            feedback_label.place(anchor = 'c', relx =0.48, rely = .91)

            clear_button = customtkinter.CTkButton(login_fields_frame, text="Add New Login",font=('Arial', 14, 'bold'), command=clear_entry_fields,
                                                   fg_color='#E97451')
            clear_button.grid(row=3, column=2, padx=10, pady=16)

            login_fields_added = True

    main_window = customtkinter.CTk()
    main_window.title('Main Application')
    main_window.after(0, lambda:main_window.state('zoomed'))
    customtkinter.set_appearance_mode("dark")

    logo_label = customtkinter.CTkLabel(main_window, image=logo_image, text='')
    logo_label.place(relx=0.5, rely=0.1, anchor='center')  

    main_application_label = customtkinter.CTkLabel(main_window, text='VAULT GUARD', text_color='white',
                                                    font=('Arial', 48))
    main_application_label.place(relx=0.5, rely=0.2, anchor='center')

    button_frame = Frame(main_window, bg= main_window.cget('bg'))  
    button_frame.place(relx=0.5, rely=0.3, anchor='center')

    add_login = customtkinter.CTkButton(button_frame, text='Add Login', fg_color='#E97451', corner_radius=5,
                                        command=add_login_fields, font=('Arial', 18))
    add_login.grid(row=0, column=0, padx=180)

    password_generator = customtkinter.CTkButton(button_frame, text='Generate Password', fg_color='#E97451',
                                                corner_radius=5, command=generate_password_gui, font=('Arial', 18))
    password_generator.grid(row=0, column=1, padx=100)

    view_account = customtkinter.CTkButton(button_frame, text='View Accounts', fg_color='#E97451',
                                        corner_radius=5, font=('Arial', 18))
    view_account.grid(row=0, column=2, padx=180)

    feedback_label = customtkinter.CTkLabel(main_window, text="")
    feedback_label.place(relx=0.5, rely=0.8, anchor='center')

    main_window.mainloop()

def save_master_password(password):
    with open(MASTER_PASSWORD_FILE, "w") as file:
        file.write(password)

def load_master_password():
    try:
        with open(MASTER_PASSWORD_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_login(site, username, password):
    with open(LOGIN_INFO_FILE, "a") as file:
        file.write(f"Site: {site}, Username/email: {username}, Password: {password}\n")

def create_new_page(root):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new page within the main window
    new_page_label = customtkinter.CTkLabel(root, text="Congratulations! Passwords accepted.")
    new_page_label.pack(pady=50)

def login():
    entered_password = entry_password.get()
    master_password = load_master_password()
    if entered_password == master_password:
        # Password correct, open the main window
        feedback_label_login.configure(text="Accepted", fg_color="green", corner_radius=8)
        login_window.destroy()
        main_application_window()
    else:
        # Password incorrect, show error message
        feedback_label_login.configure(text="Incorrect password", fg_color="red", corner_radius=8)

def toggle_password_visibility(entry):
    if entry.cget('show') == '':
        entry.configure(show='•')
    else:
        entry.configure(show='')

# Check if a master password exists
master_password = load_master_password()
if master_password:
    # If a master password exists, open the login window
    login_window = customtkinter.CTk()
    login_window.title('Login Page')
    login_window.after(0, lambda:login_window.state('zoomed'))
    customtkinter.set_appearance_mode("dark")

    text_label = customtkinter.CTkLabel(login_window, text='Welcome Back!', text_color='white', font=('Arial', 38, 'bold'))
    text_label.place(anchor = 'c', relx=0.5, rely =0.3)

    login_frame = customtkinter.CTkFrame(login_window)
    login_frame.place(anchor = 'c', relx=0.5, rely =0.5)

    text_label = customtkinter.CTkLabel(login_frame, text="Login by entering your master password", text_color='white', font=('Arial', 18, 'bold'))
    text_label.grid(row=2, column=1, pady=10)

    text_label2 = customtkinter.CTkLabel(login_frame, text="Master Password:", text_color='white', font=('Arial', 16, 'bold'))
    text_label2.grid(row=3, column=0)

    entry_password = customtkinter.CTkEntry(login_frame, show='•', width = 300)
    entry_password.grid(row=3, column=1, pady=5)

    toggle_button_login = customtkinter.CTkButton(login_frame, image=eye_image, text="", command=lambda: toggle_password_visibility(entry_password), fg_color='#E97451')
    toggle_button_login.grid(row=3, column=2, padx=5, pady=5)

    button_login = customtkinter.CTkButton(login_frame, text="Login", command=login, fg_color='#E97451', font=('Arial', 14, 'bold'))
    button_login.grid(row=4, column=1)

    feedback_label_login = customtkinter.CTkLabel(login_frame, text="", font=('Arial', 14, 'bold'))
    feedback_label_login.grid(row=5, column=1, padx=5, pady=5)


    login_window.mainloop()
else:
    # If no master password exists, open the main window to create one
    create_main_window()