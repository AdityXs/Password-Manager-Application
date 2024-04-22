from tkinter import *
import customtkinter


MASTER_PASSWORD_FILE = "master_password.txt"
LOGIN_INFO_FILE = "login_info.txt"

def main_application_window():

    login_fields_added = False  # Initialize the flag in the outer function scope

    def add_login_fields():
        nonlocal login_fields_added  # Use nonlocal to access and modify the variable from the outer scope
        if not login_fields_added:
            # Create a frame to contain the login fields and feedback label
            login_frame = Frame(main_window, bg=main_window.cget('bg'))
            login_frame.pack(side='left', pady=10, padx=100)

            login_fields_frame = Frame(login_frame, bg=main_window.cget('bg'))
            login_fields_frame.pack()

            site_label = customtkinter.CTkLabel(login_fields_frame, text="Site:", text_color='white')
            site_label.grid(row=0, column=0)

            site_entry = customtkinter.CTkEntry(login_fields_frame)
            site_entry.grid(row=0, column=1, padx=10, pady=5)

            username_label = customtkinter.CTkLabel(login_fields_frame, text="Username/email:", text_color='white')
            username_label.grid(row=1, column=0)

            username_entry = customtkinter.CTkEntry(login_fields_frame)
            username_entry.grid(row=1, column=1, padx=10, pady=5)

            password_label = customtkinter.CTkLabel(login_fields_frame, text="Password:", text_color='white')
            password_label.grid(row=2, column=0)

            password_entry = customtkinter.CTkEntry(login_fields_frame, show='•')
            password_entry.grid(row=2, column=1, padx=10, pady=5)

            def toggle_password_visibility():
                if password_entry.cget('show') == '':
                    password_entry.configure(show='•')
                else:
                    password_entry.configure(show='')

            show_hide_button = customtkinter.CTkButton(login_fields_frame, text="Show/Hide", command=toggle_password_visibility, fg_color='#E97451')
            show_hide_button.grid(row=2, column=2, padx=1, pady=5)



            def save_login_info():
                site = site_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                if site and username and password:  # Ensure all fields are filled
                    if not is_login_saved(site, username, password):  # Check if login info is already saved
                        save_login(site, username, password)  # Save login info
                        feedback_label.configure(text="Login information saved", fg_color="green", corner_radius=8)
                        save_button.configure(state=DISABLED)  # Disable the button after saving
                    else:
                        feedback_label.configure(text="Login information already saved", fg_color="red", corner_radius=8)
                else:
                    feedback_label.configure(text="Please fill in all fields", fg_color="red", corner_radius=8)

            def is_login_saved(site, username, password):
                try:
                    with open(LOGIN_INFO_FILE, "r") as file:
                        for line in file:
                            if f"Site: {site}, Username/email: {username}, Password: {password}" in line:
                                return True
                except FileNotFoundError:
                    # If the file doesn't exist, create it
                    with open(LOGIN_INFO_FILE, "w"):
                        pass  # Create an empty file
                return False


        save_button = customtkinter.CTkButton(login_fields_frame, text="Save", command=save_login_info, fg_color='#E97451')
        save_button.grid(row=3, columnspan=2, pady=10)

        # Create the feedback label inside the login frame
        feedback_label = customtkinter.CTkLabel(login_frame, text="")
        feedback_label.grid(row=4, columnspan=2, pady=10)

        login_fields_added = True  # Update the flag to indicate login fields have been added

    main_window = customtkinter.CTk()
    main_window.title('Main Application')
    main_window.geometry('1400x600')
    customtkinter.set_appearance_mode("dark")

    main_application_label = customtkinter.CTkLabel(main_window, text='Main Application', text_color='white')
    main_application_label.pack()

    # Create a frame to contain the buttons and manage their layout
    button_frame = Frame(main_window, bg=main_window.cget('bg'))
    button_frame.pack(pady=100)

    add_login = customtkinter.CTkButton(button_frame, text='Add login', fg_color='#E97451', corner_radius=5, command=add_login_fields)
    add_login.pack(side="left", padx=180)

    generate_password = customtkinter.CTkButton(button_frame, text='Generate password', fg_color='#E97451', corner_radius=5)
    generate_password.pack(side="left", padx=100)

    view_account = customtkinter.CTkButton(button_frame, text='View Accounts', fg_color='#E97451', corner_radius=5)
    view_account.pack(side="left", padx=180)

    feedback_label = customtkinter.CTkLabel(main_window, text="")
    feedback_label.pack(pady=5)

    main_window.mainloop()

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

    entry_1_frame = Frame(root, bg=root.cget('bg'))
    entry_1_frame.pack(pady=30)

    choose_password_label = customtkinter.CTkLabel(entry_1_frame, text="Choose Password:")
    choose_password_label.pack(side=LEFT, padx=(0, 10))

    entry_1 = customtkinter.CTkEntry(entry_1_frame, width=150, height=20, show='•')  # Initially hide the password
    entry_1.pack(side=LEFT)

    toggle_button_1 = customtkinter.CTkButton(entry_1_frame, text="Show/Hide", command=lambda: toggle_password_visibility(entry_1), fg_color='#E97451')
    toggle_button_1.pack(side=LEFT)

    entry_2_frame = Frame(root, bg=root.cget('bg'))
    entry_2_frame.pack(pady=30)

    confirm_password_label = customtkinter.CTkLabel(entry_2_frame, text="Confirm Password:")
    confirm_password_label.pack(side=LEFT, padx=(0, 10))

    entry_2 = customtkinter.CTkEntry(entry_2_frame, width=150, height=20, show='•')  # Initially hide the password
    entry_2.pack(side=LEFT)

    toggle_button_2 = customtkinter.CTkButton(entry_2_frame, text="Show/Hide", command=lambda: toggle_password_visibility(entry_2), fg_color='#E97451')
    toggle_button_2.pack(side=LEFT)

    checkbutton = customtkinter.CTkButton(root, text="Check", command=check_passwords, fg_color='#E97451')
    checkbutton.pack(pady=10)

    feedback_label = customtkinter.CTkLabel(root, text="")
    feedback_label.pack(pady=5)

    root.mainloop()

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
    login_window.geometry('600x200')
    customtkinter.set_appearance_mode("dark")

    label_password = customtkinter.CTkLabel(login_window, text="Enter Master Password:", text_color='white')
    label_password.pack(pady=10)

    entry_password = customtkinter.CTkEntry(login_window, show='•')
    entry_password.pack(pady=5)

    toggle_button_login = customtkinter.CTkButton(login_window, text="Show/Hide", command=lambda: toggle_password_visibility(entry_password), fg_color='#E97451')
    toggle_button_login.pack(pady=5)

    button_login = customtkinter.CTkButton(login_window, text="Login", command=login, fg_color='#E97451')
    button_login.pack(pady=5)

    feedback_label_login = customtkinter.CTkLabel(login_window, text="")
    feedback_label_login.pack(pady=5)

    login_window.mainloop()
else:
    # If no master password exists, open the main window to create one
    create_main_window()