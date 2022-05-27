from tkinter import *
from create_database import mydb, my_cursor
from functions import main_function

# Create Functions

# Login Form
def Loginform():
    global login_screen
    login_screen = Tk()
    # Setting title of screen
    login_screen.title("Login Form - PMS")
    # setting height and width of screen
    login_screen.geometry("300x230")
    login_screen.resizable(False, False)
    login_screen.eval('tk::PlaceWindow . center')

    # declaring variable
    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message = StringVar()

    # Creating log in fields and Labels
    title_label = Label(login_screen, text="PMS - Login", font=("Helvtica", 16))
    title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
    note_label = Label(login_screen, text="Please enter your credentials below", font=("Helvtica", 9), bg="#de4121",
                       fg="black")
    note_label.grid(row=1, column=0, columnspan=2, padx=20, pady=5)
    login_username_label = Label(login_screen, text="Username * ", font=("Helvtica", 9))
    login_username_label.grid(row=2, column=0, padx=20)
    login_username_box = Entry(login_screen, textvariable=username)
    login_username_box.grid(row=2, column=1, padx=20)
    login_password_label = Label(login_screen, text="Password * ", font=("Helvtica", 9))
    login_password_label.grid(row=3, column=0, padx=20, pady=5)
    login_password_box = Entry(login_screen, textvariable=password, show="*")
    login_password_box.grid(row=3, column=1, padx=20, pady=5)

    # Displaying results
    login_message_label = Label(login_screen, text="", textvariable=message)
    login_message_label.grid(row=5, column=0, columnspan=2, padx=20, pady=0)

    # Login button
    login_button = Button(login_screen, text="Login", width=10, height=1, command=login)
    login_button.grid(row=4, column=0, columnspan=2, padx=20, pady=5)
    login_screen.mainloop()


def login():
    # getting form data
    user_username = username.get()
    user_password = password.get()
    # applying empty validation
    if user_username == '' or user_password == '':
        message.set("Please fill the required fields!")
    else:
        sql_login_user = "SELECT username, password, role, username_id FROM application_users WHERE username = %s"
        username_ = (user_username,)
        my_cursor.execute(sql_login_user, username_)
        result = my_cursor.fetchall()
        if not result:
            message.set("Username not found!")
        else:
            if user_password == result[0][1]:
                message.set("Login successful")
                main_function(result[0][0], result[0][2], result[0][3], login_screen)
            else:
                message.set("Wrong username or password!")



Loginform()
