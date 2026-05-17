import tkinter as tk
from tkinter import ttk


# =========================
# functions
# =========================

def show_register():
    login_fr.pack_forget()
    main.geometry("400x500")
    register_fr.pack()

def show_login():
    register_fr.pack_forget()
    main.geometry("400x200")
    login_fr.pack()

def show_dashboard():
    login_fr.pack_forget()
    main.geometry("1200x700")
    dashboard_fr.pack(fill="both", expand=True)

# =========================
# Main Window
# =========================

main= tk.Tk()
main.title("family finance manager")
main.geometry ("400x200")


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
login_button = tk.Button (login_fr, text= "log in", padx=5, pady=5, command = show_dashboard)
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
# Dashboard Frame
# =========================

dashboard_fr = tk.Frame(main)

# Header frame
header_fr = tk.Frame (dashboard_fr, height=100 , width=1200)
header_fr.pack_propagate(False)
header_fr.pack (side= "top", fill= "both")

# header widgets
name_lbl = tk.Label(header_fr, text= "Name: Will retrieve auto", width= 30, anchor= "w", relief="groove")
username_lbl = tk.Label(header_fr, text= "Username: Will retrieve auto", width= 30, anchor= "w", relief="groove")
family_lbl = tk.Label(header_fr, text= "Family Name: Will retrieve auto" , width= 30, anchor= "w", relief="groove")
account_nm = tk.Label(header_fr, text= "Account name: Will retrieve auto" , width= 30, anchor= "w", relief="groove")
account_amount = tk.Label(header_fr, text= "example 3000:" , width= 30, anchor= "w", relief="groove")

# header position
name_lbl.grid (row= 0 , column= 0 , padx=5 , pady= 5, sticky="w")
username_lbl.grid (row= 0 , column= 1 , padx=5 , pady= 5, sticky="w")
family_lbl.grid (row= 0, column= 2, padx=5 , pady= 5, sticky="w")
account_nm.grid(row= 1 , column= 0 , padx=5 , pady= 5, sticky="w")
account_amount.grid (row= 1 , column= 1 , padx=5 , pady= 5, sticky="w")

# Navigation frame

navigation_fr = tk.Frame(dashboard_fr, width=1200 , height=50)
navigation_fr.pack_propagate(False)
navigation_fr.pack (fill= "both")

# Navigation widgets
overview_button = tk.Button (navigation_fr, text= "Overview",width= 30, anchor= "w")
account_button = tk.Button (navigation_fr, text= "Account",width= 30, anchor= "w")
expenses_button = tk.Button (navigation_fr, text= "expenses",width= 30, anchor= "w")
income_button = tk.Button (navigation_fr, text= "income",width= 30, anchor= "w")
subscription_button = tk.Button (navigation_fr, text= "subscription",width= 30, anchor= "w")

# Navigation position
overview_button.grid (row= 0 , column= 0 , padx=5 , pady= 5, sticky="w")
account_button.grid (row= 0 , column= 1 , padx=5 , pady= 5, sticky="w")
expenses_button.grid (row= 0 , column= 2 , padx=5 , pady= 5, sticky="w")
income_button.grid (row= 0 , column= 3 , padx=5 , pady= 5, sticky="w")
subscription_button.grid (row= 0 , column= 4 , padx=5 , pady= 5, sticky="w")

# =========================
# Overview Frame
# =========================

overview_fr= tk.Frame (dashboard_fr, width=1200 , height=650)
overview_fr.pack_propagate(False)
overview_fr.pack(fill= "both", expand=True)
overview_fr.columnconfigure(0,weight=1,uniform="group1")
overview_fr.columnconfigure(1,weight=1,uniform="group1")
overview_fr.rowconfigure(0, weight=1)

left_side_fr=tk.Frame(overview_fr)
left_side_fr.grid(row=0, column=0, sticky="nsew")
left_side_fr.grid_rowconfigure(0, weight=1)
left_side_fr.grid_columnconfigure(0, weight=1)


left_table = ttk.Treeview (left_side_fr,columns=("Amount" ,"Type", "Category", "Date", "User" ,), show="headings" )
left_table.heading("Amount", text= "Amount" )
left_table.heading("Type", text= "Type" )
left_table.heading("Category", text= "Category" )
left_table.heading("Date", text= "Date" )
left_table.heading("User", text= "User" )

left_table.column("Amount", stretch=True)
left_table.column("Type", stretch=True)
left_table.column("Category", stretch=True)
left_table.column("Date", stretch=True)
left_table.column("User", stretch=True)

scrollbar_y= ttk.Scrollbar (left_side_fr,orient="vertical", command= left_table.yview)
left_table.configure(yscrollcommand=scrollbar_y.set)
scrollbar_x=ttk.Scrollbar (left_side_fr,orient="horizontal", command= left_table.xview)
left_table.configure(xscrollcommand=scrollbar_x.set)
scrollbar_y.grid(row=0,column=1, sticky= "ns")
scrollbar_x.grid(row=1,column=0, sticky= "ew")

# fake data to use
random_data=[
    ("1000","income","salary","01-01-2025","alex"),
    ("1000","income","salary","01-01-2025","alex"),
    ("1000","income","salary","01-01-2025","alex"),
    ("1000","income","salary","01-01-2025","alex"),
    ("1000","income","salary","01-01-2025","alex"),
    ("1000","income","salary","01-01-2025","alex"),
]

for row in random_data:
    left_table.insert("","end", values=row )

left_table.grid(row= 0 , column= 0 , sticky= "nsew")

# future pie chart
right_side_fr=tk.Frame(overview_fr)
right_side_fr.grid(row=0, column=1, sticky="nsew")
right_side_fr.grid_rowconfigure(0, weight=1)
right_side_fr.grid_columnconfigure(0, weight=1)

chart_placeholder = tk.Label(right_side_fr, text="Future Chart Here")
chart_placeholder.pack(expand=True)

main.mainloop()
