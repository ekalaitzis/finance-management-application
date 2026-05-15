import tkinter as tk

# =========================
# functions
# =========================

def show_register():
    login_fr.pack_forget()
    register_fr.pack()

def show_login():
    register_fr.pack_forget()
    login_fr.pack()

# =========================
# Main Frame
# =========================

main= tk.Tk()
main.title("family finance manager")
main.geometry ("400x400")
main.columnconfigure(0, weight=1)
main.rowconfigure(0, weight=1)

# =========================
# Login frame
# =========================
#  frame

login_fr = tk.Frame(main)
login_fr.pack()

# variables

username_added = tk.StringVar()
password_added = tk.StringVar()

# widgets

login_title_label = tk.Label ( login_fr, text="Welcome! \n Please Enter Credentials" ,font=( "arial",18,"bold"), padx=5, pady=5 )
username_label = tk.Label(login_fr,text= "Username:", padx=5, pady=5, width=20)
username_entry = tk.Entry (login_fr, textvariable= username_added, width=20)
password_label = tk.Label(login_fr, text = "Password:", padx=5, pady=5, width=20)
password_entry= tk.Entry(login_fr, textvariable= password_added, show= "*", width=20)
login_button = tk.Button (login_fr, text= "log in", padx=5, pady=5)
register_button = tk.Button (login_fr, text= "register", command = show_register , padx=5, pady=5)

# grid
login_title_label.grid (row=0 , columnspan=4 )
username_label.grid(row = 1, column = 1)
username_entry.grid (row=1, column=2,columnspan=2)
password_label.grid(row=2,column=1)
password_entry.grid (row=2, column=2,columnspan=2)
login_button.grid (row= 4, column= 2)
register_button.grid (row= 4,column=3)


# =========================
# Register frame
# =========================

register_fr = tk.Frame(main)

# variables

username_new = tk.StringVar()
password_new = tk.StringVar()
password_new2 = tk.StringVar()

# widgets

Register_title_label = tk.Label ( register_fr, text="Account Creation\nInsert your information " ,font=( "arial",18,"bold"), padx=5, pady=5 )
new_username_label = tk.Label(register_fr,text= "Create Username:", padx=5, pady=5, width=20)
new_username_entry = tk.Entry (register_fr, textvariable=username_new, width=20)
new_password_label = tk.Label(register_fr, text = "Create Password:", padx=5, pady=5, width=20)
new_password_entry= tk.Entry(register_fr, textvariable= password_new , show= "*", width=20)
new_password2_label = tk.Label(register_fr, text = "Reenter Password:", padx=5, pady=5, width=20)
new_password2_entry= tk.Entry(register_fr, textvariable= password_new2 , show= "*", width=20)
create_button = tk.Button (register_fr, text= "Create", padx=5, pady=5)
back_button = tk.Button (register_fr, text= "Go back" , command= show_login, padx=5, pady=5)

# grid
Register_title_label.grid(row=0,columnspan=4)
new_username_label.grid(row = 1, column = 0)
new_username_entry.grid (row=1, column=1 , columnspan=2)
new_password_label.grid(row=2,column=0)
new_password_entry.grid (row=2, column=1 , columnspan=2)
new_password2_label.grid(row=3,column=0)
new_password2_entry.grid (row=3, column=1 , columnspan=2)
create_button.grid (row= 4, column= 1)
back_button.grid (row=4,column=2)
# =========================
# frame switch
# =========================

main.mainloop()
