from tkinter import *
import customtkinter
import random 
import string 
import pyperclip 
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import time 
from cryptography.fernet import Fernet


# Generate and save a key if it doesn't exist
if not os.path.exists('secret.key'):
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(data):
    return cipher_suite.decrypt(data).decode()

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
current_frame = None

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
    logo_label.pack(pady=5) 

    name_label = customtkinter.CTkLabel(root, text="VAULT GAURD", font=('arial', 48, 'bold'))
    name_label.pack(pady=5)

    instruction_label = customtkinter.CTkLabel(root, text="Sign Up", font=('arial', 28, 'bold'))
    instruction_label.pack(pady=40)

    instruction_label2 = customtkinter.CTkLabel(root, text="Create an account by entering your username and chosen password", font=('arial', 18))
    instruction_label2.pack(pady=1)

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
        # Encrypt and save the username
        encrypted_username = encrypt_data(username)
        with open('username.enc', 'wb') as file:
            file.write(encrypted_username)

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
    def save_and_encrypt_question():
        question = entry_question.get()
        answer = entry_answer.get()
        save_secret_question(question, answer)
        feedback_label.configure(text="Secret question saved successfully.", fg_color="green", corner_radius=8)
        secret_questions_window.destroy()
        main_application_window()

    def save_secret_question(question, answer):
        encrypted_question = encrypt_data(question)
        encrypted_answer = encrypt_data(answer)
        with open('secret_question.enc', 'wb') as file:
            file.write(encrypted_question + b'\n')
            file.write(encrypted_answer + b'\n')

    secret_questions_window = customtkinter.CTk()
    secret_questions_window.title("Set Secret Question")
    secret_questions_window.after(0, lambda: secret_questions_window.state('zoomed'))
    customtkinter.set_appearance_mode("dark")

    question_label = customtkinter.CTkLabel(secret_questions_window, text="Question:", font=('Arial', 18))
    question_label.place(anchor='c', relx=0.5, rely=0.3)
    entry_question = customtkinter.CTkEntry(secret_questions_window, width=300)
    entry_question.place(anchor='c', relx=0.5, rely=0.35)

    answer_label = customtkinter.CTkLabel(secret_questions_window, text="Answer:", font=('Arial', 18))
    answer_label.place(anchor='c', relx=0.5, rely=0.4)
    entry_answer = customtkinter.CTkEntry(secret_questions_window, width=300)
    entry_answer.place(anchor='c', relx=0.5, rely=0.45)

    save_button = customtkinter.CTkButton(secret_questions_window, text="Save", command=save_and_encrypt_question, fg_color='#E97451', font=('Arial', 18))
    save_button.place(anchor='c', relx=0.5, rely=0.6)

    feedback_label = customtkinter.CTkLabel(secret_questions_window, text="", font=('Arial', 18))
    feedback_label.place(anchor='c', relx=0.5, rely=0.75)

    secret_questions_window.mainloop()


def forgot_password_window():
    def reset_master_password():
        answer = entry_answer.get()
        if check_secret_answer(answer):
            new_password = entry_new_password.get()
            confirm_password = entry_confirm_password.get()
            if len(new_password) < 8:
                feedback_label.configure(text="Please choose a longer password.", fg_color="red", corner_radius=8, font=('Arial', 14, 'bold'))
            elif new_password == confirm_password:
                save_master_password(new_password)
                feedback_label.configure(text="Passwords accepted", fg_color="green", corner_radius=8, font=('Arial', 14, 'bold'))
                forgot_password.destroy()
            else:
                feedback_label.configure(text="Passwords do not match", fg_color="red", corner_radius=8, font=('Arial', 14, 'bold'))
        else:
            feedback_label.configure(text="Incorrect answer to secret question", fg_color="red", corner_radius=8, font=('Arial', 14, 'bold'))

    def load_secret_question():
        try:
            with open('secret_question.enc', 'rb') as file:
                encrypted_question = file.readline().strip()
                encrypted_answer = file.readline().strip()

            question = decrypt_data(encrypted_question)
            answer = decrypt_data(encrypted_answer)

            return question, answer
        except FileNotFoundError:
            return None, None
        except Exception as e:
            print(e)
            return None, None

    def check_secret_answer(answer):
        try:
            _, saved_answer = load_secret_question()
            return answer == saved_answer
        except Exception as e:
            print(e)
            return False
    
    def toggle_password_visibility(entry):
        if entry.cget('show') == '•':
            entry.configure(show='')
        else:
            entry.configure(show='•')

    forgot_password = customtkinter.CTk()
    forgot_password.title("Forgot Password")
    forgot_password.after(0, lambda: forgot_password.state('zoomed'))
    customtkinter.set_appearance_mode("dark")

    try:
        question, _ = load_secret_question()
    except Exception as e:
        print(e)
        question = "Question not set"

    instruction_label = customtkinter.CTkLabel(forgot_password, text="Answer your secret question to reset your password", font=('Arial', 48, 'bold')) 
    instruction_label.place(anchor='c', relx=0.5, rely=0.2)

    question_label = customtkinter.CTkLabel(forgot_password, text=question, font=('Arial', 18))
    question_label.place(anchor='c', relx=0.5, rely=0.3)
    entry_answer = customtkinter.CTkEntry(forgot_password, width=300)
    entry_answer.place(anchor='c', relx=0.5, rely=0.35)

    new_password_label = customtkinter.CTkLabel(forgot_password, text="New Password:", font=('Arial', 18))
    new_password_label.place(anchor='c', relx=0.5, rely=0.5)

    entry_new_password = customtkinter.CTkEntry(forgot_password, width=300, show='•')
    entry_new_password.place(anchor='c', relx=0.5, rely=0.55)
    toggle_new_password_btn = customtkinter.CTkButton(forgot_password, width=50, command=lambda: toggle_password_visibility(entry_new_password))
    toggle_new_password_btn.place(anchor='c', relx=0.73, rely=0.55)

    confirm_password_label = customtkinter.CTkLabel(forgot_password, text="Confirm Password:", font=('Arial', 18))
    confirm_password_label.place(anchor='c', relx=0.5, rely=0.6)
    entry_confirm_password = customtkinter.CTkEntry(forgot_password, width=300, show='•')
    entry_confirm_password.place(anchor='c', relx=0.5, rely=0.65)
    toggle_confirm_password_btn = customtkinter.CTkButton(forgot_password, width=50, command=lambda: toggle_password_visibility(entry_confirm_password))
    toggle_confirm_password_btn.place(anchor='c', relx=0.73, rely=0.65)

    reset_button = customtkinter.CTkButton(forgot_password, text="Reset Password", command=reset_master_password, fg_color='#E97451', font=('Arial', 18))
    reset_button.place(anchor='c', relx=0.5, rely=0.7)

    feedback_label = customtkinter.CTkLabel(forgot_password, text="", font=('Arial', 18))
    feedback_label.place(anchor='c', relx=0.5, rely=0.75)

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
        try:
            # Attempt to retrieve and convert input to an integer
            password_length = int(length_entry.get())

            # Check if the input is within the valid range
            if password_length <= 0 or password_length > 27:
                feedback_label.configure(text="Please enter an integer below 28", fg_color="red", corner_radius=8)
                return

            password_chars = string.ascii_letters
            if include_numbers.get():
                password_chars += string.digits
            if include_special_chars.get():
                password_chars += string.punctuation

            password = ''.join(random.choice(password_chars) for i in range(password_length))

            password_label.configure(text=password)
            feedback_label.configure(text="Password generated successfully", fg_color="green", corner_radius=8, font=('arial', 14, 'bold'))
            feedback_label.place(relx=0.5, rely=0.75)
        except ValueError:
            # If conversion to integer fails (e.g., non-numeric input)
            feedback_label.configure(text="Please enter a valid integer", fg_color="red", corner_radius=8, font=('arial', 14, 'bold'))
            feedback_label.place(relx=0.5, rely=0.75)

    def copy_password():
        password = password_label.cget('text')
        pyperclip.copy(password)
        messagebox.showinfo('Password Copied', 'The password has been copied to the clipboard')

    def generate_password_gui():
        nonlocal password_generator_added

        if not password_generator_added:
            global length_entry, include_numbers, include_special_chars, password_label

            password_gen_frame = customtkinter.CTkFrame(main_window)  
            password_gen_frame.place(relx=0.5, rely=0.51, anchor='center')
            

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

    def clear_frame():
        global current_frame
        if current_frame:
            current_frame.destroy()
            current_frame = None

    def view_accounts():
        global current_frame, accounts_label

        # Clear any existing frame
        clear_frame()

        # Get the background color of the main application window
        app_bg_color = main_window.cget("bg")

        # Create a canvas and a scrollbar
        accounts_canvas = customtkinter.CTkCanvas(main_window, bg=app_bg_color, width=400, height=300)
        accounts_canvas.place(relx=0.625, rely=0.35, anchor='nw', relwidth=0.23, relheight=0.3)

        scrollbar = Scrollbar(main_window, command=accounts_canvas.yview)
        scrollbar.place(relx=0.846, rely=0.35, anchor='nw', relheight=0.3)  # Adjust the height to match the canvas

        # Configure the canvas to use the scrollbar
        accounts_canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        current_frame = customtkinter.CTkFrame(accounts_canvas, width=400, height=300)
        accounts_canvas.create_window((0, 0), window=current_frame, anchor='nw', tags="frame_window")

        def on_canvas_configure(event):
            # Adjust the frame width to match the canvas width
            canvas_width = event.width
            accounts_canvas.itemconfig("frame_window", width=canvas_width)
            accounts_canvas.config(scrollregion=accounts_canvas.bbox("all"))

        accounts_canvas.bind("<Configure>", on_canvas_configure)

        # Add the accounts_label to the frame
        accounts_label = customtkinter.CTkLabel(current_frame, text="Saved Logins", font=("Arial", 16, 'bold'))
        accounts_label.pack()

        try:
            for filename in os.listdir(LOGIN_INFO_DIR):
                with open(os.path.join(LOGIN_INFO_DIR, filename), "rb") as file:
                    encrypted_site = file.readline().strip()
                    site_name = decrypt_data(encrypted_site)
                    site_label = customtkinter.CTkButton(current_frame, text=site_name, font=("Arial", 12, 'bold'), fg_color="#E97451", cursor="hand2")
                    site_label.pack(padx=20, pady=3)
                    site_label.bind("<Button-1>", lambda event, site_name=site_name: show_login_details(site_name))

        except FileNotFoundError:
            pass  # No login info files yet

        # Update the scroll region
        current_frame.update_idletasks()
        accounts_canvas.config(scrollregion=accounts_canvas.bbox("all"))

    def show_login_details(site_text):
        global current_frame, login_details_label, back_button, edit_button, delete_button

        # Clear any existing frame
        clear_frame()

        # Create a new frame with the same dimensions as view_accounts frame
        current_frame = customtkinter.CTkFrame(main_window)
        current_frame.place(relx=0.625, rely=0.35, anchor='nw', relwidth=0.23, relheight=0.3)

        accounts_label = customtkinter.CTkLabel(current_frame, text="Login Details", font=("Arial", 16, 'bold'))
        accounts_label.pack()

        # Find the matching login file
        for filename in os.listdir(LOGIN_INFO_DIR):
            with open(os.path.join(LOGIN_INFO_DIR, filename), "rb") as file:
                encrypted_site = file.readline().strip()
                site = decrypt_data(encrypted_site)
                if site == site_text:
                    encrypted_username = file.readline().strip()
                    encrypted_password = file.readline().strip()
                    username = decrypt_data(encrypted_username)
                    password = decrypt_data(encrypted_password)
                    content = f"Site: {site}\nUsername/email: {username}\nPassword: "

                    # Create label to display site and username
                    login_details_label = customtkinter.CTkLabel(current_frame, text=content, justify=LEFT)
                    login_details_label.pack(anchor=W, padx=20)

                    # Create label to display the password (initially hidden)
                    password_label = customtkinter.CTkLabel(current_frame, text="•" * len(password), justify=LEFT)
                    password_label.pack(anchor=W, padx=20)

                    def toggle_password_visibility():
                        if password_label.cget("text") == "•" * len(password):
                            password_label.configure(text=password)
                            toggle_button.configure(text="Hide Password")
                        else:
                            password_label.configure(text="•" * len(password))
                            toggle_button.configure(text="Show Password")

                    # Button to toggle password visibility
                    toggle_button = customtkinter.CTkButton(current_frame, text="Show Password", command=toggle_password_visibility)
                    toggle_button.pack(pady=5)

                    # Edit button to edit login details
                    edit_button = customtkinter.CTkButton(current_frame, text="Edit", command=lambda: edit_login_details(filename, site, username, password))
                    edit_button.pack(padx=5, pady=6)

                    # Delete button to delete the login details
                    delete_button = customtkinter.CTkButton(current_frame, text="Delete", command=lambda: delete_login(filename))
                    delete_button.pack(pady=5)

                    # Back button to return to initial view
                    back_button = customtkinter.CTkButton(current_frame, text="Back", command=view_accounts)
                    back_button.pack(padx=5, pady=5)
                    break

    def delete_login(filename):
        # Remove the file
        os.remove(os.path.join(LOGIN_INFO_DIR, filename))
        # Provide feedback to the user
        feedback_label = customtkinter.CTkLabel(main_window, text="Login deleted successfully!", font=("Arial", 14, 'bold'), fg_color="red", corner_radius=8)
        feedback_label.place(relx=0.68, rely=0.656)
        # Return to the accounts view
        view_accounts()



    def edit_login_details(filename, site, username, password):
        global current_frame

        # Clear any existing frame
        clear_frame()

        # Create a new frame with the same dimensions as view_accounts frame
        current_frame = customtkinter.CTkFrame(main_window)
        current_frame.place(relx=0.625, rely=0.35, anchor='nw', relwidth=0.23, relheight=0.3)

        site_label = customtkinter.CTkLabel(current_frame, text="Site:", font=("Arial", 14))
        site_label.pack(pady=5)
        site_entry = customtkinter.CTkEntry(current_frame, width=300)
        site_entry.insert(0, site)
        site_entry.pack(pady=5)

        username_label = customtkinter.CTkLabel(current_frame, text="Username/Email:", font=("Arial", 14))
        username_label.pack(pady=5)
        username_entry = customtkinter.CTkEntry(current_frame, width=300)
        username_entry.insert(0, username)
        username_entry.pack(pady=5)

        password_label = customtkinter.CTkLabel(current_frame, text="Password:", font=("Arial", 14))
        password_label.pack(pady=5)
        password_entry = customtkinter.CTkEntry(current_frame, width=300)
        password_entry.insert(0, password)
        password_entry.pack(pady=5)


        def save_edited_details():
            new_site = site_entry.get()
            new_username = username_entry.get()
            new_password = password_entry.get()

            encrypted_site = encrypt_data(new_site)
            encrypted_username = encrypt_data(new_username)
            encrypted_password = encrypt_data(new_password)

            # Save the new details
            new_filename = os.path.join(LOGIN_INFO_DIR, f"{new_site}.txt")
            with open(new_filename, "wb") as file:
                file.write(encrypted_site + b'\n')
                file.write(encrypted_username + b'\n')
                file.write(encrypted_password + b'\n')

            # Delete the old file if the filename has changed
            if new_site != site:
                os.remove(os.path.join(LOGIN_INFO_DIR, filename))

            feedback_label = customtkinter.CTkLabel(main_window, text="Details updated successfully!", font=("Arial", 14, 'bold'), fg_color="green", corner_radius=8)
            feedback_label.place(relx=0.68, rely=0.656)

        save_button = customtkinter.CTkButton(current_frame, text="Save", command=save_edited_details)
        save_button.pack(pady=10)

        back_button = customtkinter.CTkButton(current_frame, text="Back", command=view_accounts)
        back_button.pack(pady=5)

    def add_login_fields():
        nonlocal login_fields_added
        if not login_fields_added:


            # Validation function to limit input length
            def limit_size_input(input_str):
                return len(input_str) <= 28

            vcmd = (main_window.register(lambda input_str: limit_size_input(input_str)), '%P')

            # Create the actual frame inside the border frame
            login_fields_frame = customtkinter.CTkFrame(main_window, width=450, height=80)  
            login_fields_frame.place(relx=0.26, rely=0.443, anchor='center')
        
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
    add_login.grid(row=0, column=0, padx=200)

    password_generator = customtkinter.CTkButton(button_frame, text='Generate Password', fg_color='#E97451',
                                                corner_radius=5, command=generate_password_gui, font=('Arial', 18))
    password_generator.grid(row=0, column=1, padx=100)

    view_account = customtkinter.CTkButton(button_frame, text='View Accounts', fg_color='#E97451',
                                        corner_radius=5, font=('Arial', 18), command=view_accounts)
    view_account.grid(row=0, column=2, padx=200)

    feedback_label = customtkinter.CTkLabel(main_window, text="")
    feedback_label.place(relx=0.5, rely=0.8, anchor='center')

    main_window.mainloop()

def save_master_password(password):
    # Encrypt and save the master password
    encrypted_password = encrypt_data(password)
    with open('master_password.enc', 'wb') as file:
        file.write(encrypted_password)

def load_username():
    # Load and decrypt the username
    try:
        with open('username.enc', 'rb') as file:
            encrypted_username = file.read()
        return decrypt_data(encrypted_username)
    except Exception as e:
        print(e)
        return None

def load_master_password():
    # Load and decrypt the master password
    try:
        with open('master_password.enc', 'rb') as file:
            encrypted_password = file.read()
        return decrypt_data(encrypted_password)
    except Exception as e:
        print(e)
        return None

def save_login(site, username, password):
    filename = generate_filename(site, username)
    encrypted_site = encrypt_data(site)
    encrypted_username = encrypt_data(username)
    encrypted_password = encrypt_data(password)
    with open(filename, "wb") as file:
        file.write(encrypted_site + b'\n')
        file.write(encrypted_username + b'\n')
        file.write(encrypted_password + b'\n')


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

    logo_image = customtkinter.CTkImage(Image.open(file_path + "/image.png"), size=(140, 140))
        
    logo_label = customtkinter.CTkLabel(root, image=logo_image, text='')
    logo_label.pack(pady=10)  

    name_label = customtkinter.CTkLabel(root, text="VAULT GAURD", font=('arial', 48, 'bold'))
    name_label.pack(pady=10)

    label1 = customtkinter.CTkLabel(root, text='Login Here', font=('Arial', 28, 'bold'))
    label1.pack(pady=40)

    label2 = customtkinter.CTkLabel(root, text='Enter your username and password to log in', font=('Arial', 18))
    label2.pack(pady=10)    


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

    login_button = customtkinter.CTkButton(root, text="Login", command=lambda: check_login(username_entry.get(), entry_1.get(), root), fg_color='#E97451', font=('Arial', 18, 'bold'))
    login_button.pack(pady=160)

    forgot_password_label = customtkinter.CTkButton(root, text="Forgot Password?", font=('arial', 18, 'bold'), fg_color='blue', corner_radius=8)
    forgot_password_label.pack(pady=1)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    feedback_label = customtkinter.CTkLabel(root, text="", font=('Arial', 18))
    feedback_label.pack(pady=11)

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