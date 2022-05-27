from tkinter import *
from tkinter import ttk
import random
import datetime
import pwnedpasswords
from tkinter.messagebox import showinfo
from settings import lowercase, symbol, uppercase, numbers
from create_database import mydb, my_cursor
from authentication import encrypt_password, decrypt_password



def main_function(username_, role, user_id, login_screen):
    login_screen.destroy()
    global id_
    id_ = user_id
    global user
    user = username_
    global user_role
    user_role = role
    root = Tk()
    root.title('Software Application')
    root.geometry("950x400")
    root.resizable(True, True)
    root.eval('tk::PlaceWindow . center')

    # Export to CSV
    def export_csv():
        password_count = password_count_box.get()
        password_count = int(password_count)
        now = datetime.datetime.now()
        current_time = now.strftime("%H_%M_%S")
        try:
            output_file = open("Batch_Password-" + current_time + ".csv", "w")
            for i in range(password_count):
                bpassword = autogenerate()
                # write string to the file
                output_file.write(bpassword + "\n")
                # close file
            output_file.close()
            clear_fields()
            batch_win.destroy()
        except EXCEPTION as e:
            showinfo("Error!", e)

    # Batch Passwords
    def batch_password():
        global batch_win
        batch_win = Tk()
        batch_win.title('Batch Generation')
        batch_win.geometry("300x70")
        batch_win.eval('tk::PlaceWindow . center')

        # Create Main Form to Enter Data
        global password_count_box
        password_count = Label(batch_win, text="Numbers of Passwords:").grid(row=0, column=0, sticky=W, padx=10)
        password_count_box = Entry(batch_win)
        password_count_box.grid(row=0, column=1, pady=5)

        save_export_record = Button(batch_win, text="Save and Export to CSV", command=export_csv)
        save_export_record.grid(row=1, column=0, padx=10)

    # Autogenerate Password
    def autogenerate():
        password_box.delete(0, END)
        sql4 = "SELECT uppercase, lowercase, symbols, numbers FROM complexity WHERE complexity_id = 1"
        result4 = my_cursor.execute(sql4)
        result4 = my_cursor.fetchall()
        password_length = result4[0][0] + result4[0][1] + result4[0][2] + result4[0][3]
        password_check = 1
        password = [None] * password_length  # Password string is set to empty
        while password_check == 1:
            for i in range(result4[0][0]):
                random_placeholder = random.randrange(1, password_length, 1)
                random_character = random.randrange(1, 26, 1)
                password[random_placeholder] = uppercase[random_character]
            for i in range(result4[0][1]):
                random_placeholder = random.randrange(1, password_length, 1)
                while password[random_placeholder] is not None:
                    random_placeholder = random.randrange(1, password_length, 1)
                random_character = random.randrange(1, 26, 1)
                password[random_placeholder] = lowercase[random_character]
            for i in range(result4[0][2]):
                random_placeholder = random.randrange(1, password_length, 1)
                while password[random_placeholder] is not None:
                    random_placeholder = random.randrange(1, password_length, 1)
                random_character = random.randrange(1, 10, 1)
                password[random_placeholder] = symbol[random_character]
            for i in range(password_length):
                if password[i] is None:
                    random_character = random.randrange(1, 10, 1)
                    password[i] = numbers[random_character]

            final_password = ""

            for i in password:
                final_password += i
            password_box.insert(0, final_password)
            password_check = pwnedpasswords.check(final_password, plain_text=True)

        assert password_check == 0
        print("Secured Password!")
        return final_password

    # Check Pwned Passwords
    def check_pwned_password(password):
        x = pwnedpasswords.check(password, plain_text=True)
        return x

    # Modify Complixity Function
    def modify_complixity():
        sql3 = "SELECT uppercase, lowercase, symbols, numbers FROM complexity WHERE complexity_id = 1"
        result3 = my_cursor.execute(sql3)
        result3 = my_cursor.fetchall()

        def update_complexity():
            sql_command = """UPDATE complexity SET uppercase = %s, lowercase = %s, numbers = %s, symbols = %s WHERE complexity_id = 1"""
            uppercase = uppercase_edit.get()
            lowercase = lowercase_edit.get()
            numbers = numbers_edit.get()
            symbols = symbols_edit.get()

            inputs = (uppercase, lowercase, numbers, symbols)

            my_cursor.execute(sql_command, inputs)

            mydb.commit()
            list_records()
            complixity_win.destroy()

        complixity_win = Tk()
        complixity_win.title('Modify Complixity')
        complixity_win.geometry("300x150")
        complixity_win.eval('tk::PlaceWindow . center')

        # Create Main Form to Enter Data
        id_label = Label(complixity_win, text="Uppercase:").grid(row=0, column=0, sticky=W, padx=10)
        application_label = Label(complixity_win, text="Lowercase:").grid(row=1, column=0, sticky=W, padx=10)
        username_label = Label(complixity_win, text="Numbers:").grid(row=2, column=0, sticky=W, padx=10)
        password_label = Label(complixity_win, text="Symbols:").grid(row=3, column=0, sticky=W, padx=10)

        global uppercase_edit
        global lowercase_edit
        global numbers_edit
        global symbols_edit
        # Create Entry Boxes
        uppercase_edit = Entry(complixity_win)
        uppercase_edit.grid(row=0, column=1, pady=5)
        uppercase_edit.insert(0, result3[0][0])

        lowercase_edit = Entry(complixity_win)
        lowercase_edit.grid(row=1, column=1, pady=5)
        lowercase_edit.insert(0, result3[0][1])

        numbers_edit = Entry(complixity_win)
        numbers_edit.grid(row=2, column=1, pady=5)
        numbers_edit.insert(0, result3[0][2])

        symbols_edit = Entry(complixity_win)
        symbols_edit.grid(row=3, column=1, pady=5)
        symbols_edit.insert(0, result3[0][3])

        save_record = Button(complixity_win, text="Update Complexity", command=update_complexity)
        save_record.grid(row=4, column=0, padx=10)

    # Create Clear Text Fields Function
    def clear_fields():
        application_box.delete(0, END)
        username_box.delete(0, END)
        password_box.delete(0, END)

    def check_manual_complexity(password):
        sql4 = "SELECT uppercase, lowercase, symbols, numbers FROM complexity WHERE complexity_id = 1"
        result4 = my_cursor.execute(sql4)
        result4 = my_cursor.fetchall()
        password_length = result4[0][0] + result4[0][1] + result4[0][2] + result4[0][3]

        lowercount = 0
        uppercasecount = 0
        symbolcount = 0
        numbercount = 0
        for i in range(len(lowercase)):
            lowercount = lowercount + password.count(lowercase[i])

        for i in range(len(uppercase)):
            uppercasecount = uppercasecount + password.count(uppercase[i])

        for i in range(len(symbol)):
            symbolcount = symbolcount + password.count(symbol[i])

        for i in range(len(numbers)):
            numbercount = numbercount + password.count(numbers[i])

        if uppercasecount >= result4[0][0] and lowercount >= result4[0][1] and symbolcount >= result4[0][
            2] and numbercount >= result4[0][3]:
            return 1
        else:
            return 0

    def add_record():
        sql_command = "INSERT INTO users (application, username, password, key_string, addedby) VALUES (%s, %s, %s, %s, %s)"
        result_encrypt = encrypt_password(password_box.get())
        values = (application_box.get(), username_box.get(), result_encrypt[0], result_encrypt[1], id_)
        if len(application_box.get()) == 0 or len(username_box.get()) == 0 or len(password_box.get()) == 0:
            showinfo("Error: Missing Fields", "Please make sure you fill all required fields.")
            assert application_box.get() is not None
            assert username_box.get() is not None
            assert password_box.get() is not None
            print("Fields are empty")

        else:
            print(password_box.get())
            com_check = check_manual_complexity(password_box.get())
            if com_check == 0:
                showinfo("Password Complexity!", "Your password doesn't comply to the system complexity")
            else:
                check = check_pwned_password(password_box.get())
                if check >= 1:
                    showinfo("Warning: Leaked Password",
                             "You chose a leaked password, Please choose a different password!")
                else:
                    my_cursor.execute(sql_command, values)
                    # Commit the changes to Database
                    mydb.commit()
                    # Clear the fields
                    clear_fields()
                    list_records()

    # Create Search record
    def search_record():
        def search_now():

            for widget in frm.winfo_children():
                widget.destroy()

            selected = drop.get()
            sql = ""

            if selected == "Application Name":
                sql = "SELECT user_id, application, username FROM users WHERE application = %s"
            if selected == "Username":
                sql = "SELECT user_id, application, username FROM users WHERE username = %s"
            if selected == "UserID":
                sql = "SELECT user_id, application, username FROM users WHERE user_id = %s"
            searched = search_box.get()
            # sql = "SELECT user_id, application, username, password FROM users WHERE username = %s"
            name = (searched,)
            result = my_cursor.execute(sql, name)
            result = my_cursor.fetchall()

            userid_frm_label = Label(frm, text="ID", font=('Helvetica', 8, 'bold')).grid(row=0, column=0, sticky=W,
                                                                                         padx=10)
            application_frm_label = Label(frm, text="Application Name", font=('Helvetica', 8, 'bold')).grid(row=0,
                                                                                                            column=1,
                                                                                                            sticky=W,
                                                                                                            padx=10)
            username_frm_label = Label(frm, text="Username", font=('Helvetica', 8, 'bold')).grid(row=0, column=2,
                                                                                                 sticky=W, padx=10)
            password_frm_label = Label(frm, text="Password", font=('Helvetica', 8, 'bold')).grid(row=0, column=3,
                                                                                                 sticky=W, padx=10)
            action_frm_label = Label(frm, text="Action", font=('Helvetica', 8, 'bold')).grid(row=0, column=4, sticky=W,
                                                                                             padx=10)

            if not result:
                result = "Record Not Found ..."
                lookup_label = Label(frm, text=result)
                lookup_label.grid(row=1, column=0, columnspan=7, sticky=W, padx=10)
            else:

                for index, x in enumerate(result):
                    num = 0
                    index += 1
                    id_reference = str(x[0])
                    for y in x:
                        lookup_label = Label(frm, text=y)
                        lookup_label.grid(row=index, column=num, sticky=W, padx=10)
                        lookup_label = Label(frm, text="******")
                        lookup_label.grid(row=index, column=3, sticky=W, padx=10)
                        num += 1
                    frm_button = Frame(frm, padx=5, pady=5)
                    frm_button.grid(row=index, column=num + 2, sticky=E + W + N + S)
                    edit_button = Button(frm_button, text="Edit",
                                         command=lambda id_reference=id_reference: edit_now(id_reference, index))
                    edit_button.grid(row=0, column=1, sticky=W, padx=3)
                    delete_button = Button(frm_button, text="Delete")
                    delete_button.grid(row=0, column=2, sticky=W)

        if user_role == 1:
            assert user_role == 1
            print("User is an admin user")
            # Entry box for search record
            search_box = Entry(root)
            search_box.grid(row=3, column=1, padx=10, pady=10)
            # search button for record
            search_button = Button(root, text="Search", command=search_now)
            search_button.grid(row=3, column=2, sticky=W, padx=10)
            Display_all = Button(root, text="Clear Search", command=list_records)
            Display_all.grid(row=3, column=3, sticky=W, padx=0)
            # Create Drop down box
            drop = ttk.Combobox(root, value=["Search by ...", "Application Name", "Username", "UserID"])
            drop.current(0)
            drop.grid(row=3, column=0, padx=20)

    # Edit Now Function
    def edit_now(id_reference, index):

        sql2 = "SELECT user_id, application, username, password, key_string FROM users WHERE user_id = %s"
        name2 = (id_reference,)
        result2 = my_cursor.execute(sql2, name2)
        result2 = my_cursor.fetchall()
        pass_decrypt = decrypt_password(result2[0][3].encode(), result2[0][4].encode())

        def update():
            sql_command = """UPDATE users SET application = %s, username = %s, password = %s, key_string = %s WHERE user_id = %s"""
            user_id = id_box_edit.get()
            application = application_box_edit.get()
            username = username_box_edit.get()
            password = password_box_edit.get()
            result_encrypt = encrypt_password(password)
            inputs = (application, username, result_encrypt[0], result_encrypt[1], user_id)

            my_cursor.execute(sql_command, inputs)

            mydb.commit()
            list_records()
            edit_win.destroy()

        edit_win = Tk()
        edit_win.title('Software Application - Edit Record')
        edit_win.geometry("400x160")
        edit_win.eval('tk::PlaceWindow . center')

        # Create Main Form to Enter Data
        id_label = Label(edit_win, text="ID:").grid(row=index + 1, column=0, sticky=W, padx=10)
        application_label = Label(edit_win, text="Application Name:").grid(row=index + 2, column=0, sticky=W, padx=10)
        username_label = Label(edit_win, text="Username:").grid(row=index + 3, column=0, sticky=W, padx=10)
        password_label = Label(edit_win, text="Password:").grid(row=index + 4, column=0, sticky=W, padx=10)

        global id_box_edit
        global application_box_edit
        global password_box_edit
        global username_box_edit
        # Create Entry Boxes
        id_box_edit = Entry(edit_win)
        id_box_edit.grid(row=index + 1, column=1, pady=5)
        id_box_edit.insert(0, result2[0][0])
        id_box_edit.config(state="disabled")

        application_box_edit = Entry(edit_win)
        application_box_edit.grid(row=index + 2, column=1, pady=5)
        application_box_edit.insert(0, result2[0][1])

        username_box_edit = Entry(edit_win)
        username_box_edit.grid(row=index + 3, column=1, pady=5)
        username_box_edit.insert(0, result2[0][2])

        password_box_edit = Entry(edit_win)
        password_box_edit.grid(row=index + 4, column=1, pady=5)
        password_box_edit.insert(0, pass_decrypt)

        save_record = Button(edit_win, text="Update Record", command=update)
        save_record.grid(row=index + 5, column=0, padx=10)

    # Create List Records Function
    def list_records():
        # Query the database
        if user_role == 0:
            my_cursor.execute("SELECT user_id, application, username from users WHERE addedby = " + str(id_))
            result = my_cursor.fetchall()
            my_cursor.execute(
                "SELECT user_id, application, username, password, key_string from users WHERE addedby = " + str(id_))
            result_flagged = my_cursor.fetchall()
        if user_role == 1:
            my_cursor.execute("SELECT user_id, application, username from users")
            result = my_cursor.fetchall()
            my_cursor.execute("SELECT user_id, application, username, password, key_string from users")
            result_flagged = my_cursor.fetchall()

        global frm

        frm = Frame(root, highlightbackground="black", highlightthickness=1, padx=5, pady=5)
        frm.grid(row=4, column=0, columnspan=8, padx=20, sticky=E + W + N + S)

        frm.rowconfigure(0, weight=1)
        frm.columnconfigure(0, weight=1)

        frm.rowconfigure(1, weight=1)
        frm.columnconfigure(1, weight=1)

        frm.rowconfigure(2, weight=1)
        frm.columnconfigure(2, weight=1)

        frm.rowconfigure(3, weight=1)
        frm.columnconfigure(3, weight=1)
        frm.rowconfigure(4, weight=1)
        frm.columnconfigure(4, weight=1)

        userid_frm_label = Label(frm, text="ID", font=('Helvetica', 8, 'bold')).grid(row=0, column=0, sticky=W, padx=10)
        application_frm_label = Label(frm, text="Application Name", font=('Helvetica', 8, 'bold')).grid(row=0, column=1,
                                                                                                        sticky=W,
                                                                                                        padx=10)
        username_frm_label = Label(frm, text="Username", font=('Helvetica', 8, 'bold')).grid(row=0, column=2, sticky=W,
                                                                                             padx=10)
        password_frm_label = Label(frm, text="Password", font=('Helvetica', 8, 'bold')).grid(row=0, column=3, sticky=W,
                                                                                             padx=10)
        action_frm_label = Label(frm, text="Note", font=('Helvetica', 8, 'bold')).grid(row=0, column=4, sticky=W,
                                                                                       padx=10)
        action_frm_label = Label(frm, text="Action", font=('Helvetica', 8, 'bold')).grid(row=0, column=5, sticky=W,
                                                                                         padx=10)

        for index, x in enumerate(result):
            num = 0
            index += 1
            id_reference = str(x[0])
            for y in x:
                lookup_label = Label(frm, text=y)
                lookup_label.grid(row=index, column=num, sticky=W, padx=10)
                lookup_label = Label(frm, text="******")
                lookup_label.grid(row=index, column=3, sticky=W, padx=10)
                num += 1
            # Create Frame for button
            frm_button = Frame(frm, padx=5, pady=5)
            frm_button.grid(row=index, column=num + 2, sticky=E + W + N + S)
            edit_button = Button(frm_button, text="Edit",
                                 command=lambda id_reference=id_reference: edit_now(id_reference, index))
            edit_button.grid(row=0, column=1, sticky=W, padx=3)
            delete_button = Button(frm_button, text="Delete",
                                   command=lambda id_reference=id_reference: remove_one(id_reference, index))
            delete_button.grid(row=0, column=2, sticky=W)

        # Flagged Password
        for index, x in enumerate(result_flagged):
            num = 0
            index += 1
            hashed_pass = str(x[3])
            key_pass = str(x[4])
            pass_decrypt = decrypt_password(hashed_pass.encode(), key_pass.encode())

            check = check_manual_complexity(pass_decrypt.decode())
            if check == 0:
                lookup_label = Label(frm, text="Should Be Replaced", bg="red")
                lookup_label.grid(row=index, column=4, sticky=W, padx=10)
            else:
                lookup_label = Label(frm, text="Password is Okay", bg="green")
                lookup_label.grid(row=index, column=4, sticky=W, padx=10)

    # Delete Record from DB
    def remove_one(id_reference, index):
        sql2 = "SELECT user_id, application, username, password FROM users WHERE user_id = %s"
        name2 = (id_reference,)
        result2 = my_cursor.execute(sql2, name2)
        result2 = my_cursor.fetchall()
        selection_id = result2[0][0]
        sql_command = "DELETE FROM users WHERE user_id = " + str(selection_id) + ";"
        my_cursor.execute(sql_command)
        # Commit the changes to Database
        mydb.commit()
        # Clear the fields
        list_records()

    # Create a Label
    title_label = Label(root, text="PMS - Password Management System", font=("Helvtica", 16))
    title_label.grid(row=0, column=0, columnspan=5, pady=10, sticky=W, padx=10)

    if user_role == 0:
        frm_welcome = Frame(root, padx=0, pady=0)
        frm_welcome.grid(row=0, column=6, sticky=E + W + N + S)
        phrase = "Welcome " + str(user)
        welcome_label = Label(frm_welcome, text=phrase, font=("Helvtica", 9))
        welcome_label.grid(row=0, column=0, columnspan=2, pady=2, sticky=W, padx=10)

        phrase_role = "You're a Legacy user"
        role_label = Label(frm_welcome, text=phrase_role, font=("Helvtica", 6))
        role_label.grid(row=1, column=0, columnspan=2, pady=2, sticky=W, padx=10)

    complixity = Button(root, text="Modify Complixity", font=("Helvtica", 7), command=modify_complixity)
    batch_password = Button(root, text="Batch Password", font=("Helvtica", 7), command=batch_password)
    if user_role == 1:
        complixity.grid(row=0, column=7, sticky=E + W + N + S, padx=0, pady=10)
        batch_password.grid(row=0, column=6, sticky=E + W + N + S, padx=0, pady=10)
    else:
        complixity.grid_forget()
        batch_password.forget()

    # Create Main Form to Enter Data
    application_label = Label(root, text="Application Name:").grid(row=1, column=0, sticky=E, padx=10)
    username_label = Label(root, text="Username:").grid(row=1, column=2, sticky=W, padx=10)
    password_label = Label(root, text="Password:").grid(row=1, column=4, sticky=W, padx=10)

    # Create Entry Boxes
    application_box = Entry(root)
    application_box.grid(row=1, column=1, pady=5)

    username_box = Entry(root)
    username_box.grid(row=1, column=3, pady=5)

    global password_box
    password_box = Entry(root)
    password_box.grid(row=1, column=5, pady=5)

    # Create Buttons
    add_record = Button(root, text="Add Record", command=add_record)
    add_record.grid(row=1, column=6, padx=10, pady=10)

    clear_fields_button = Button(root, text="Auto-Generate", command=autogenerate)
    clear_fields_button.grid(row=1, column=7)

    # list users
    search_record()
    list_records()
    root.mainloop()
