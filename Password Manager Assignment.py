from tkinter import *
import customtkinter
import random 
import string 
import pyperclip 
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import time 

#Loading Images
file_path = os.path.dirname(os.path.realpath(__file__))
eye_image = customtkinter.CTkImage(Image.open(file_path +
                                              "/eye open.png"), size =(35, 35))

logo_image = customtkinter.CTkImage(Image.open(file_path +
                                              "/image.png"), size =(35, 35))

copy_image = customtkinter.CTkImage(Image.open(file_path +
                                              "/copy 2.png"), size =(35, 35))


MASTER_PASSWORD_FILE = "master_password.txt"
LOGIN_INFO_FILE = "login_info.txt"
LOGIN_INFO_DIR = "logins"
USERNAME_FILE = "username.txt"



if not os.path.exists(LOGIN_INFO_DIR):
    os.makedirs(LOGIN_INFO_DIR)

# Global variables to hold references to widgets
main_application_window = None
accounts_frame = None
accounts_label = None
login_details_label = None
back_button = None

def generate_filename(site, username):
    timestamp = int(time.time())
    filename = f"{site}_{username}_{timestamp}.txt"
    return os.path.join(LOGIN_INFO_DIR, filename)

def create_main_window():
    root = customtkinter.CTk()

    root.title('Sign Up Page')
    root.after(0, lambda: root.state('zoomed'))

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme('blue')

    logo_image = customtkinter.CTkImage(Image.open(file_path + "/image.png"), size=(140, 140))
        
    logo_label = customtkinter.CTkLabel(root, image=logo_image, text='')
    logo_label.place(relx=0.5, rely=0.1, anchor='center')  

    name_label = customtkinter.CTkLabel(root, text="VAULT GAURD", font=('arial', 48, 'bold'))
    name_label.place(anchor='c', relx=0.5, rely=0.2)

    instruction_label = customtkinter.CTkLabel(root, text="Sign Up", font=('arial', 28, 'bold'))
    instruction_label.place(anchor='c', relx=0.5, rely=0.29)

    instruction_label2 = customtkinter.CTkLabel(root, text="Create an account by entering your username and chosen password", font=('arial', 18))
    instruction_label2.place(anchor='c', relx=0.5, rely=0.33)

    def check_passwords():
        username = username_entry.get()  # Get the username from the entry widget
        password1 = entry_1.get()
        password2 = entry_2.get()
        if len(password1) < 8 or len(password2) < 8:
            feedback_label.configure(text="Please choose a longer password", fg_color="red", corner_radius=8)
        elif password1 == password2:
            feedback_label.configure(text="Accepted", fg_color="green", corner_radius=8)
            # Save master password
            save_master_password(password1)
            # Save username
            save_username(username)  # Call function to save username
            # Once passwords are accepted, open the secret questions page
            root.destroy()
            set_secret_questions_window()
        else:
            feedback_label.configure(text="Passwords Do Not Match", fg_color="red", corner_radius=8)

    def save_username(username):
        with open("username.txt", "w") as file:  # Create or overwrite a file to save the username
            file.write(username)

    def toggle_password_visibility(entry):
        if entry.cget('show') == '':
            entry.configure(show='•')
        else:
            entry.configure(show='')
    
    def limit_entry_length(entry_widget, max_length):
        def check_length(event):
            current_text = entry_widget.get()
            if len(current_text) > max_length:
                entry_widget.delete(max_length, len(current_text))
        return check_length

    max_length = 28

    username_frame = customtkinter.CTkFrame(root)
    username_frame.place(anchor='c', relx=0.5, rely=0.45)

    choose_username = customtkinter.CTkLabel(username_frame, text="Username:", font=('Arial', 18))
    choose_username.grid(row=0, column=0, padx=20, pady=10)

    username_entry = customtkinter.CTkEntry(username_frame, width=200, height=30)
    username_entry.grid(row=0, column=1, padx=5, pady=10)

    # Bind the entry widget to limit the length of input
    username_entry.bind("<KeyRelease>", limit_entry_length(username_entry, max_length))
        
    choose_password_label = customtkinter.CTkLabel(username_frame, text="Choose Password:", font = ('Arial', 18))
    choose_password_label.grid(row=1, column=0, padx=20, pady=10)

    entry_1 = customtkinter.CTkEntry(username_frame, width=200, height=30, show='•')  # Initially hide the password
    entry_1.grid(row=1, column=1, padx=20, pady=10)

    toggle_button_1 = customtkinter.CTkButton(username_frame, image = eye_image, text="", command=lambda: toggle_password_visibility(entry_1), fg_color='#E97451')
    toggle_button_1.grid(row=1, column=2, padx=20, pady=10)

    confirm_password_label = customtkinter.CTkLabel(username_frame, text="Confirm Password:", font = ('Arial', 18))
    confirm_password_label.grid(row=2, column=0, padx=20, pady=10)

    entry_2 = customtkinter.CTkEntry(username_frame, width=200, height=30, show='•')  # Initially hide the password
    entry_2.grid(row=2, column=1, padx=20, pady=10)

    toggle_button_2 = customtkinter.CTkButton(username_frame, image = eye_image, text="", command=lambda: toggle_password_visibility(entry_2), fg_color='#E97451')
    toggle_button_2.grid(row=2, column=2, padx=20, pady=10)

    checkbutton = customtkinter.CTkButton(root, text="Check", command=check_passwords, fg_color='#E97451', font = ('Arial', 18))
    checkbutton.place(anchor='c', relx=0.5, rely=0.58)

    feedback_label = customtkinter.CTkLabel(root, text="", font=('arial', 18))
    feedback_label.place(anchor='c', relx=0.5, rely=0.63)

    root.mainloop()

def set_secret_questions_window():
    def save_secret_questions():
        question1 = entry_question1.get()
        answer1 = entry_answer1.get()
        question2 = entry_question2.get()
        answer2 = entry_answer2.get()
        if question1 and answer1 and question2 and answer2:
            with open("secret_questions.txt", "w") as file:
                file.write(f"Question 1: {question1}\nAnswer 1: {answer1}\n")
                file.write(f"Question 2: {question2}\nAnswer 2: {answer2}\n")
            messagebox.showinfo("Success", "Secret questions saved successfully.")
            secret_questions_window.destroy()
            main_application_window()
        else:
            feedback_label.configure(text="Please fill in all fields", fg_color="red", corner_radius=8)

    secret_questions_window = customtkinter.CTk()
    secret_questions_window.title("Set Secret Questions")
    secret_questions_window.after(0, lambda: secret_questions_window.state('zoomed'))
    customtkinter.set_appearance_mode("dark")

    question1_label = customtkinter.CTkLabel(secret_questions_window, text="Question 1:", font=('Arial', 18))
    question1_label.place(anchor='c', relx=0.5, rely=0.3)
    entry_question1 = customtkinter.CTkEntry(secret_questions_window, width=300)
    entry_question1.place(anchor='c', relx=0.5, rely=0.35)

    answer1_label = customtkinter.CTkLabel(secret_questions_window, text="Answer 1:", font=('Arial', 18))
    answer1_label.place(anchor='c', relx=0.5, rely=0.4)
    entry_answer1 = customtkinter.CTkEntry(secret_questions_window, width=300)
    entry_answer1.place(anchor='c', relx=0.5, rely=0.45)

    question2_label = customtkinter.CTkLabel(secret_questions_window, text="Question 2:", font=('Arial', 18))
    question2_label.place(anchor='c', relx=0.5, rely=0.5)
    entry_question2 = customtkinter.CTkEntry(secret_questions_window, width=300)
    entry_question2.place(anchor='c', relx=0.5, rely=0.55)

    answer2_label = customtkinter.CTkLabel(secret_questions_window, text="Answer 2:", font=('Arial', 18))
    answer2_label.place(anchor='c', relx=0.5, rely=0.6)
    entry_answer2 = customtkinter.CTkEntry(secret_questions_window, width=300)
    entry_answer2.place(anchor='c', relx=0.5, rely=0.65)

    save_button = customtkinter.CTkButton(secret_questions_window, text="Save", command=save_secret_questions, fg_color='#E97451', font=('Arial', 18))
    save_button.place(anchor='c', relx=0.5, rely=0.7)

    feedback_label = customtkinter.CTkLabel(secret_questions_window, text="", font=('arial', 18))
    feedback_label.place(anchor='c', relx=0.5, rely=0.75)

    secret_questions_window.mainloop()

def forgot_password_window():
    def reset_master_password():
        answer1 = entry_answer1.get()
        answer2 = entry_answer2.get()
        if check_secret_answers(answer1, answer2):
            new_password = entry_new_password.get()
            confirm_password = entry_confirm_password.get()
            if new_password == confirm_password:
                save_master_password(new_password)
                feedback_label.configure(text="Passwords accepted", fg_color="green", corner_radius=8)
                forgot_password.destroy()
            else:
                feedback_label.configure(text="Passwords do not match", fg_color="red", corner_radius=8)
        else:
            feedback_label.configure(text="Incorrect answers to secret questions", fg_color="red", corner_radius=8)

    def check_secret_answers(answer1, answer2):
        try:
            with open("secret_questions.txt", "r") as file:
                data = file.readlines()
                saved_answer1 = data[1].split(":")[1].strip()
                saved_answer2 = data[3].split(":")[1].strip()
                return answer1 == saved_answer1 and answer2 == saved_answer2
        except Exception as e:
            print(e)
            return False
    
    def toggle_password_visibility(entry, button):
        if entry.cget('show') == '•':
            entry.configure(show='')
            button.configure(text='Hide')
        else:
            entry.configure(show='•')
            button.configure(text='Show')

    forgot_password = customtkinter.CTk()
    forgot_password.title("Forgot Password")
    forgot_password.after(0, lambda: forgot_password.state('zoomed'))
    customtkinter.set_appearance_mode("dark")


    try:
        with open("secret_questions.txt", "r") as file:
            data = file.readlines()
            saved_question1 = data[0].split(":")[1].strip()
            saved_question2 = data[2].split(":")[1].strip()
    except Exception as e:
        print(e)
        saved_question1 = "Question 1 not set"
        saved_question2 = "Question 2 not set"

    instruction_label = customtkinter.CTkLabel(forgot_password, text="Answer your secret questions to reset your password", font=('Arial', 18))
    instruction_label.place(anchor='c', relx=0.5, rely=0.2)

    question1_label = customtkinter.CTkLabel(forgot_password, text=saved_question1, font=('Arial', 18))
    question1_label.place(anchor='c', relx=0.5, rely=0.3)
    entry_answer1 = customtkinter.CTkEntry(forgot_password, width=300)
    entry_answer1.place(anchor='c', relx=0.5, rely=0.35)

    question2_label = customtkinter.CTkLabel(forgot_password, text=saved_question2, font=('Arial', 18))
    question2_label.place(anchor='c', relx=0.5, rely=0.5)
    entry_answer2 = customtkinter.CTkEntry(forgot_password, width=300)
    entry_answer2.place(anchor='c', relx=0.5, rely=0.55)

    new_password_label = customtkinter.CTkLabel(forgot_password, text="New Password:", font=('Arial', 18))
    new_password_label.place(anchor='c', relx=0.5, rely=0.7)

    entry_new_password = customtkinter.CTkEntry(forgot_password, width=300, show='•')
    entry_new_password.place(anchor='c', relx=0.5, rely=0.75)
    toggle_new_password_btn = customtkinter.CTkButton(forgot_password, text="Show", width=50, command=lambda: toggle_password_visibility(entry_new_password, toggle_new_password_btn))
    toggle_new_password_btn.place(anchor='c', relx=0.73, rely=0.75)

    confirm_password_label = customtkinter.CTkLabel(forgot_password, text="Confirm Password:", font=('Arial', 18))
    confirm_password_label.place(anchor='c', relx=0.5, rely=0.8)
    entry_confirm_password = customtkinter.CTkEntry(forgot_password, width=300, show='•')
    entry_confirm_password.place(anchor='c', relx=0.5, rely=0.85)
    toggle_confirm_password_btn = customtkinter.CTkButton(forgot_password, text="Show", width=50, command=lambda: toggle_password_visibility(entry_confirm_password, toggle_confirm_password_btn))
    toggle_confirm_password_btn.place(anchor='c', relx=0.73, rely=0.85)

    reset_button = customtkinter.CTkButton(forgot_password, text="Reset Password", command=reset_master_password, fg_color='#E97451', font=('Arial', 18))
    reset_button.place(anchor='c', relx=0.5, rely=0.9)


    feedback_label = customtkinter.CTkLabel(forgot_password, text="", font=('Arial', 18))
    feedback_label.place(anchor='c', relx=0.5, rely=0.95)

    forgot_password.mainloop()

def main_application_window():
    # Loading Images
    file_path = os.path.dirname(os.path.realpath(__file__))
    eye_image = customtkinter.CTkImage(Image.open(file_path + "/eye open.png"), size=(35, 35))
    logo_image = customtkinter.CTkImage(Image.open(file_path + "/image.png"), size=(130, 130))
    copy_image = customtkinter.CTkImage(Image.open(file_path + "/copy 2.png"), size=(35, 35))

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
            password_gen_frame.place(relx=0.5, rely=0.54, anchor='center')
            

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

    
    def view_accounts():
        global accounts_frame, accounts_label

        # Destroy previous accounts_frame if it exists
        if accounts_frame:
            accounts_frame.destroy()

        # Get the background color of the main application window
        app_bg_color = main_window.cget("bg")

        # Create a canvas and a scrollbar
        accounts_canvas = customtkinter.CTkCanvas(main_window, bg=app_bg_color, width=400, height=300)
        accounts_canvas.place(relx=0.68, rely=0.35, anchor='nw')

        scrollbar = Scrollbar(main_window, command=accounts_canvas.yview)
        scrollbar.place(relx=0.88, rely=0.35, anchor='nw', height=300)  # Adjust the height to match the canvas

        # Configure the canvas to use the scrollbar
        accounts_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        accounts_frame = customtkinter.CTkFrame(accounts_canvas, width=400, height=300)
        accounts_canvas.create_window((0, 0), window=accounts_frame, anchor='nw', tags="frame_window")

        def on_canvas_configure(event):
            # Adjust the frame width to match the canvas width
            canvas_width = event.width
            accounts_canvas.itemconfig("frame_window", width=canvas_width)
            accounts_canvas.config(scrollregion=accounts_canvas.bbox("all"))

        accounts_canvas.bind("<Configure>", on_canvas_configure)

        # Add the accounts_label to the frame
        accounts_label = customtkinter.CTkLabel(accounts_frame, text="Saved Logins", font=("Arial", 16, 'bold'))
        accounts_label.pack()

        try:
            for filename in os.listdir(LOGIN_INFO_DIR):
                with open(os.path.join(LOGIN_INFO_DIR, filename), "r") as file:
                    content = file.read()
                    site_name = content.split("\n")[0].split(": ")[1]
                    site_label = customtkinter.CTkButton(accounts_frame, text=site_name, font=("Arial", 12, 'bold'), fg_color="#E97451", cursor="hand2")
                    site_label.pack(anchor=W, padx=20, pady=3)
                    site_label.bind("<Button-1>", lambda event, site_name=site_name: show_login_details(site_name))

        except FileNotFoundError:
            pass  # No login info files yet

        # Update the scroll region
        accounts_frame.update_idletasks()
        accounts_canvas.config(scrollregion=accounts_canvas.bbox("all"))

    def show_login_details(site_text):
        global accounts_frame, login_details_label, back_button

        # Destroy previous accounts_frame if exists
        if accounts_frame:
            accounts_frame.destroy()

        # Create a new frame with the same dimensions as view_accounts frame
        accounts_frame = customtkinter.CTkFrame(main_window, width=400, height=300)
        accounts_frame.place(relx=0.68, rely=0.35, anchor='nw')

        accounts_label = customtkinter.CTkLabel(accounts_frame, text="Login Details", font=("Arial", 16, 'bold'))
        accounts_label.pack()

        # Find the matching login file
        for filename in os.listdir(LOGIN_INFO_DIR):
            with open(os.path.join(LOGIN_INFO_DIR, filename), "r") as file:
                content = file.read()
                if f"Site: {site_text}" in content:
                    login_details_label = customtkinter.CTkLabel(accounts_frame, text=content, justify=LEFT)
                    login_details_label.pack(anchor=W, padx=20)

                    # Back button to return to initial view
                    back_button = customtkinter.CTkButton(accounts_frame, text="Back", command=view_accounts)
                    back_button.pack(pady=10)
                    break

        def back_to_accounts():
            global accounts_frame
            if accounts_frame:
                accounts_frame.destroy()
            view_accounts()

    def add_login_fields():
        nonlocal login_fields_added
        if not login_fields_added:


            # Validation function to limit input length
            def limit_size_input(input_str):
                return len(input_str) <= 28

            vcmd = (main_window.register(lambda input_str: limit_size_input(input_str)), '%P')

            # Create the actual frame inside the border frame
            login_fields_frame = customtkinter.CTkFrame(main_window, width=450, height=80)  
            login_fields_frame.place(relx=0.23, rely=0.45, anchor='center')
        
            site_label = customtkinter.CTkLabel(login_fields_frame, text="Site:", text_color='white', font=('Arial', 14, 'bold'))
            site_label.grid(row=0, column=0)

            site_entry = customtkinter.CTkEntry(login_fields_frame, width = 250, validate='key', validatecommand=vcmd)
            site_entry.grid(row=0, column=1, padx=10, pady=10)

            username_label = customtkinter.CTkLabel(login_fields_frame, text="Username/email:", text_color='white', font=('Arial', 14, 'bold'))
            username_label.grid(row=1, column=0, padx=10)

            username_entry = customtkinter.CTkEntry(login_fields_frame, width = 250, validate='key', validatecommand=vcmd)
            username_entry.grid(row=1, column=1, padx=10, pady=5)

            password_label = customtkinter.CTkLabel(login_fields_frame, text="Password:", text_color='white', font=('Arial', 14, 'bold'))
            password_label.grid(row=2, column=0)

            password_entry = customtkinter.CTkEntry(login_fields_frame, show='•', width = 250, validate='key', validatecommand=vcmd)
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
                        feedback_label.configure(text="Login information already saved", fg_color="red", corner_radius=8)
                else:
                    feedback_label.configure(text="Please fill in all fields", fg_color="red", corner_radius=8)

            def is_login_saved(site, username, password):
                try:
                    for filename in os.listdir(LOGIN_INFO_DIR):
                        with open(os.path.join(LOGIN_INFO_DIR, filename), "r") as file:
                            content = file.read()
                            if f"Site: {site}\nUsername/email: {username}\nPassword: {password}" in content:
                                return True
                except FileNotFoundError:
                    os.makedirs(LOGIN_INFO_DIR)
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

    main_application_label = customtkinter.CTkLabel(main_window, text= "VAULT GAURD", text_color='white',
                                                    font=('Arial', 48))
    main_application_label.place(relx=0.5, rely=0.2, anchor='center')

    button_frame = Frame(main_window, bg= main_window.cget('bg'))  
    button_frame.place(relx=0.5, rely=0.33, anchor='center')

    add_login = customtkinter.CTkButton(button_frame, text='Add Login', fg_color='#E97451', corner_radius=5,
                                        command=add_login_fields, font=('Arial', 18))
    add_login.grid(row=0, column=0, padx=180)

    password_generator = customtkinter.CTkButton(button_frame, text='Generate Password', fg_color='#E97451',
                                                corner_radius=5, command=generate_password_gui, font=('Arial', 18))
    password_generator.grid(row=0, column=1, padx=100)

    view_account = customtkinter.CTkButton(button_frame, text='View Accounts', fg_color='#E97451',
                                        corner_radius=5, font=('Arial', 18), command=view_accounts)
    view_account.grid(row=0, column=2, padx=180)

    feedback_label = customtkinter.CTkLabel(main_window, text="")
    feedback_label.place(relx=0.5, rely=0.8, anchor='center')

    main_window.mainloop()

def save_master_password(password):
    with open(MASTER_PASSWORD_FILE, "w") as file:
        file.write(password)

def load_username():
    try:
        with open(USERNAME_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def load_master_password():
    try:
        with open(MASTER_PASSWORD_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_login(site, username, password):
    filename = generate_filename(site, username)
    with open(filename, "w") as file:
        file.write(f"Site: {site}\nUsername/email: {username}\nPassword: {password}\n")

def create_new_page(root):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new page within the main window
    new_page_label = customtkinter.CTkLabel(root, text="Congratulations! Passwords accepted.")
    new_page_label.pack(pady=50)

def check_login(username, password, root):
    master_password = load_master_password()
    username = load_username
    if username == username and password == master_password:
        feedback_label.configure(text="Login Successful", fg_color="green", corner_radius=8)
        # Proceed with successful login actions
        root.destroy()  # Close the login window
        main_application_window()  # Open the main window
    else:
        feedback_label.configure(text="Invalid Username or Password", fg_color="red", corner_radius=8)




def toggle_password_visibility(entry):
    if entry.cget('show') == '':
        entry.configure(show='•')
    else:
        entry.configure(show='')

def load_username():
    try:
        with open("username.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "User"  # Default value if the file does not exist or username is not found

# Check if a master password exists
master_password = load_master_password()
if master_password:
    root = customtkinter.CTk()
    root.title('Login Page')
    root.after(0, lambda: root.state('zoomed'))
    customtkinter.set_appearance_mode("dark")

    label1 = customtkinter.CTkLabel(root, text='Login Here', font=('Arial', 48))
    label1.place(relx=0.44, rely=0.3)


    def toggle_password_visibility(entry):
        if entry.cget('show') == '':
            entry.configure(show='•')
        else:
            entry.configure(show='')

    def forgot_password():
        root.destroy()
        forgot_password_window()

    def limit_entry_length(entry_widget, max_length):
        def check_length(event):
            current_text = entry_widget.get()
            if len(current_text) > max_length:
                entry_widget.delete(max_length, len(current_text))
        return check_length

    max_length = 28
    username_frame = customtkinter.CTkFrame(root)
    username_frame.place(anchor='c', relx=0.5, rely=0.45)

    choose_username = customtkinter.CTkLabel(username_frame, text="Username:", font=('Arial', 18))
    choose_username.grid(row=0, column=0, padx=20, pady=10)
    username_entry = customtkinter.CTkEntry(username_frame, width=200, height=30)
    username_entry.grid(row=0, column=1, padx=5, pady=10)
    username_entry.bind("<KeyRelease>", limit_entry_length(username_entry, max_length))

    password_label = customtkinter.CTkLabel(username_frame, text="Password:", font=('Arial', 18))
    password_label.grid(row=1, column=0, padx=20, pady=10)
    entry_1 = customtkinter.CTkEntry(username_frame, width=200, height=30, show='•')
    entry_1.grid(row=1, column=1, padx=20, pady=10)
    toggle_button = customtkinter.CTkButton(username_frame, image=eye_image, text="", command=lambda: toggle_password_visibility(entry_1), fg_color='#E97451')
    toggle_button.grid(row=1, column=2, padx=20, pady=10)

    login_button = customtkinter.CTkButton(root, text="Login", command=lambda: check_login(username_entry.get(), entry_1.get(), root), fg_color='#E97451', font=('Arial', 18))
    login_button.place(anchor='c', relx=0.5, rely=0.58)

    forgot_password_label = customtkinter.CTkLabel(root, text="Forgot Password?", font=('arial', 14), fg_color='blue', corner_radius=8)
    forgot_password_label.place(anchor='c', relx=0.5, rely=0.7)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    feedback_label = customtkinter.CTkLabel(root, text="", font=('Arial', 18))
    feedback_label.place(anchor='c', relx=0.5, rely=0.65)

    root.mainloop()



else:
    # If no master password exists, open the main window to create one
    create_main_window()



def save_master_password(password):
    with open(MASTER_PASSWORD_FILE, "w") as file:
        file.write(password)

def load_master_password():
    try:
        with open(MASTER_PASSWORD_FILE, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None