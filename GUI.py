import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import Financial as be
import charts as chart
import datetime




user_ID_number=0
category_map_name_id = {}
category_map_id_name = {}
category_list = []
transaction_type_list = ["INCOME","EXPENSE"]
overview_transactions_list = []
flr_date_to= datetime.datetime.today().date()
flr_date_from= flr_date_to.replace(day=1)
flr_date_to = flr_date_to.strftime("%d-%m-%Y")
flr_date_from = flr_date_from.strftime("%d-%m-%Y")
selected_item_from_table = None
selected_values_from_table = None
# =========================
# functions
# =========================

def show_register():
    login_fr.pack_forget()
    main.geometry("400x300")
    register_fr.pack()

def show_login():
    register_fr.pack_forget()
    main.geometry("400x200")
    login_fr.pack()

def show_dashboard():

    if be.Member.validateMember(username_added.get(),password_added.get()):
        user_information = be.Member.getMemberByUsername(username_added.get())
        global user_ID_number
        user_ID_number= user_information[0]
        login_fr.pack_forget()
        main.geometry("1200x600")
        dashboard_fr.pack(fill="both", expand=True)
        name_lbl.configure(text="Name: "+ user_information[1] + " " + user_information[2])
        username_lbl.configure(text= "Username: " + user_information[3] )
      #  user_id.configure(text= "User ID: " + str(user_information[0]))
        income_amount.configure(text= "Income: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"INCOME")) )
        expenses_amount.configure(text= "Expenses: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"EXPENSE")))
        collect_category_per_user(user_ID_number)
        collect_all_transactions_per_user(user_ID_number,flr_date_from,flr_date_to)
        chart.income_vrs_expenses(top_right_side_fr, user_ID_number)

    else:
        messagebox.showerror("Login Error", "Username or password is wrong.\nPlease try again.")
        username_label.configure(fg="red")
        password_label.configure(fg="red")


def show_overview():
    overview_fr.tkraise()
    for widget in top_right_side_fr.winfo_children():
        widget.destroy()
    chart.income_vrs_expenses(top_right_side_fr, user_ID_number)

def show_income():
    income_fr.tkraise()

def show_expenses():
    for widget in top_right_side_fr.winfo_children():
        widget.destroy()
    chart.expenses_pie_chart(top_right_side_fr,user_ID_number)
    collect_all_expenses_per_user(user_ID_number,flr_date_from,flr_date_to)

def show_subscription():
    subscription_fr.tkraise()

def new_registration():
    new_username_label.configure(fg="black")
    new_first_name_label.configure(fg="black")
    new_last_name_label.configure(fg="black")
    new_password_label.configure(fg="black")
    new_password2_label.configure(fg="black")
    if first_name.get().strip() == "" or last_name.get().strip() == "" or username_new.get().strip() == "" or password_new.get().strip()=="" or password_new2.get().strip()=="":
        messagebox.showerror("Empty Fields", "Please add all the required fields.")
        new_username_label.configure(fg="red")
        new_first_name_label.configure(fg="red")
        new_last_name_label.configure(fg="red")
        new_password_label.configure(fg="red")
        new_password2_label.configure(fg="red")
    else:
        if password_new.get() == password_new2.get():
            new_user = be.Member(first_name.get(), last_name.get(), username_new.get(), password_new.get())
            success = new_user.createMember()

            if success:
                show_login()
                first_name.set("")
                last_name.set("")
                username_new.set("")
                password_new.set("")
                password_new2.set("")
            else:
                messagebox.showerror("Registration Failed", "User couldn't be created, \nPlease choose an other Username ")
                new_username_label.configure(fg="red")
        else:
            messagebox.showerror("Password Error", "Passwords do not match.")
            new_password_label.configure(fg= "red")
            new_password2_label.configure(fg="red")

def number_validation(value):# use to check the number is positive float
    try:
        amount_valid=float(value)

        if amount_valid >= 0 :
            return True
        else:
            return False

    except ValueError:
        return False

def collect_category_per_user (User_id):
    full_list = be.Category.getAllCategoriesByMemberId(User_id)
    global category_map_name_id,category_map_id_name
    for category_id,category_name,member_id in full_list:
        category_map_name_id[category_name]=category_id
        category_map_id_name[category_id]=category_name
        category_list.append(category_name)
    transaction_category_entry ["values"]=category_list

def collect_all_transactions_per_user (user_id,date_from,date_to):
    global overview_transactions_list
    overview_transactions_list.clear()
    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    overview_transactions_list.extend(be.Transaction.getAllTransactionsByMemberIdFilterDate(user_id,iso_date_from,iso_date_to))
    overview_transactions_list = [(t[0],t[1],t[2],datetime.datetime.strptime(t[3], "%Y-%m-%d").strftime("%d-%m-%Y"),t[4]) for t in overview_transactions_list]
    for item in left_table.get_children():
        left_table.delete(item)
    for row_row in overview_transactions_list:
        left_table.insert("", "end", values=row_row)
#    print(overview_transactions_list)
#    print ( "DATE FROM " +str (date_from) + "TO " +str (date_to))

def collect_all_expenses_per_user (user_id, date_from,date_to):
    global overview_transactions_list
    overview_transactions_list.clear()
    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    overview_transactions_list.extend(be.Transaction.getAllTransactionsByMemberIdFilterDate(user_id,iso_date_from,iso_date_to))
    overview_transactions_list = [(t[0],t[1],t[2],datetime.datetime.strptime(t[3], "%Y-%m-%d").strftime("%d-%m-%Y"),t[4]) for t in overview_transactions_list]
    for item in left_table.get_children():
        left_table.delete(item)
    for row_row in overview_transactions_list:
        if row_row [1] == "INCOME":
            continue
        left_table.insert("", "end", values=row_row)



def add_transaction():
    if transaction_name_vr.get().strip() == "" or transaction_type_vr.get().strip() == "" or transaction_amount_vr.get().strip() == "" or transaction_category_vr.get().strip()=="" or transaction_category_entry.get() not in category_list or transaction_type_entry.get() not in transaction_type_list:
        messagebox.showerror("Empty Fields", "Please add all the required fields.")
        transaction_amount_lbl.configure(fg= "red")
        transaction_name_lbl.configure(fg= "red")
        transaction_category_lbl.configure(fg= "red")
        transaction_type_lbl.configure(fg= "red")
    elif not number_validation(transaction_amount_vr.get()):
        messagebox.showerror("Wrong Amount", "Please ensure you add a valid amount.\nEx:5.76")
        transaction_amount_lbl.configure(fg= "red")
        transaction_name_lbl.configure(fg= "black")
        transaction_category_lbl.configure(fg= "black")
        transaction_type_lbl.configure(fg= "black")
    else:
        transaction_amount_lbl.configure(fg= "black")
        transaction_name_lbl.configure(fg= "black")
        transaction_category_lbl.configure(fg= "black")
        transaction_type_lbl.configure(fg= "black")
        selected_category_id = category_map_name_id[transaction_category_vr.get()]
        iso_date = datetime.datetime.strptime(transaction_date_entry.get(),"%d-%m-%Y").date().isoformat()
        new_transaction=be.Transaction(transaction_name_vr.get(),transaction_type_vr.get(),transaction_amount_vr.get(), iso_date,selected_category_id)
        new_transaction.createTransactionByCategoryId(selected_category_id)
        collect_all_transactions_per_user(user_ID_number,flr_date_from,flr_date_to)
        chart.income_vrs_expenses(top_right_side_fr, user_ID_number)
        income_amount.configure(text= "Income: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"INCOME")) )
        expenses_amount.configure(text= "Expenses: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"EXPENSE")))
        transaction_amount_vr.set("")
        transaction_name_vr.set("")
        transaction_category_vr.set("")
        transaction_type_vr.set("")
        transaction_date_entry.set_date(datetime.date.today())

def filter_button_refresh ():
    global flr_date_from , flr_date_to
    flr_date_from = date_from_ENTRY.get()
    flr_date_to = date_to_ENTRY.get()
    collect_all_transactions_per_user(user_ID_number,flr_date_from,flr_date_to)

def left_click(event):
    item = left_table.identify_row(event.y)
    left_table.selection_set(item)

def right_click (event):
    global selected_item_from_table , selected_values_from_table
    selected_item_from_table = left_table.identify_row(event.y)
    if not selected_item_from_table:
        return


    left_table.selection_set(selected_item_from_table)
    selected_values_from_table = left_table.item(selected_item_from_table , "values")
    right_click_menu.post(event.x_root, event.y_root)

def delete_item():
    print (selected_values_from_table)
def edit_item():
    pass

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

login_title_label = tk.Label ( login_fr, text="Welcome!\nPlease Enter Credentials" ,font=( "arial",18,"bold"), padx=5, pady=5 )
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

first_name = tk.StringVar()
last_name = tk.StringVar()
username_new = tk.StringVar()
password_new = tk.StringVar()
password_new2 = tk.StringVar()

# widgets

Register_title_label = tk.Label ( register_fr, text="Account Creation\nInsert your information " ,font=( "arial",18,"bold"), padx=5, pady=5 )
new_username_label = tk.Label(register_fr,text= "New Username:", padx=5, pady=5, width=20)
new_username_entry = tk.Entry (register_fr, textvariable=username_new, width=20)
new_password_label = tk.Label(register_fr, text = "Create Password:", padx=5, pady=5, width=20)
new_password_entry= tk.Entry(register_fr, textvariable= password_new , show= "*", width=20)
new_password2_label = tk.Label(register_fr, text = "Reenter Password:", padx=5, pady=5, width=20)
new_password2_entry= tk.Entry(register_fr, textvariable= password_new2 , show= "*", width=20)
new_first_name_label = tk.Label(register_fr, text = "First Name:", padx=5, pady=5, width=20)
new_first_name_entry= tk.Entry(register_fr, textvariable= first_name , width=20)
new_last_name_label = tk.Label(register_fr, text = "Last Name:", padx=5, pady=5, width=20)
new_last_name_entry= tk.Entry(register_fr, textvariable= last_name , width=20)
create_button = tk.Button (register_fr, text= "Create", padx=5, pady=5, command=new_registration )
back_button = tk.Button (register_fr, text= "Go back" , command= show_login, padx=5, pady=5)

# grid
Register_title_label.grid(row=0,columnspan=4)
new_first_name_label.grid(row = 1, column = 0)
new_first_name_entry.grid(row=1, column=1 , columnspan=2)
new_last_name_label.grid(row=2,column=0)
new_last_name_entry.grid(row=2, column=1 , columnspan=2)
new_username_label.grid(row = 3, column = 0)
new_username_entry.grid (row=3, column=1 , columnspan=2)
new_password_label.grid(row=4,column=0)
new_password_entry.grid (row=4, column=1 , columnspan=2)
new_password2_label.grid(row=5,column=0)
new_password2_entry.grid (row=5, column=1 , columnspan=2)
create_button.grid (row= 6, column= 1)
back_button.grid (row=6,column=2)

# =========================
# Dashboard Frame
# =========================

dashboard_fr = tk.Frame(main)

# Header frame
header_fr = tk.Frame (dashboard_fr, height=50 , width=1200)
header_fr.pack_propagate(False)
header_fr.pack (side= "top", fill= "both")

# header widgets
name_lbl = tk.Label(header_fr, text= "Name: Will retrieve auto", width= 30, anchor= "w", relief="groove")
username_lbl = tk.Label(header_fr, text= "Username: Will retrieve auto", width= 30, anchor= "w", relief="groove")
#user_id = tk.Label(header_fr, text= "UserId: Will retrieve auto" , width= 30, anchor= "w", relief="groove")
income_amount = tk.Label(header_fr, text= "Income:" , width= 30, anchor= "w", relief="groove")
expenses_amount = tk.Label(header_fr, text= "Expenses:" , width= 30, anchor= "w", relief="groove")
overview_button = tk.Button (header_fr, text= "Overview",width= 30, anchor= "w", command= show_overview )
expenses_button = tk.Button (header_fr, text= "expenses",width= 30, anchor= "w", command=show_expenses)
income_button = tk.Button (header_fr, text= "income",width= 30, anchor= "w" , command= show_income)
subscription_button = tk.Button (header_fr, text= "subscription",width= 30, anchor= "w", command=show_subscription)

# header position
name_lbl.grid (row= 0 , column= 0 , padx=5 , pady= 5, sticky="w")
username_lbl.grid (row= 0 , column= 1 , padx=5 , pady= 5, sticky="w")
#user_id.grid (row= 0, column= 0, padx=5 , pady= 5, sticky="w")
income_amount.grid (row= 1 , column= 0 , padx=5 , pady= 5, sticky="w")
expenses_amount.grid (row= 1 , column= 1 , padx=5 , pady= 5, sticky="w")
overview_button.grid (row= 0 , column= 2 , padx=5 , pady= 5, sticky="w")
expenses_button.grid (row= 1 , column= 2 , padx=5 , pady= 5, sticky="w")
income_button.grid (row= 1 , column= 3 , padx=5 , pady= 5, sticky="w")
subscription_button.grid (row= 0 , column= 3 , padx=5 , pady= 5, sticky="w")

# filter frame

filter_fr = tk.Frame(dashboard_fr, width=1200 , height=50)
filter_fr.pack_propagate(False)
filter_fr.pack (fill= "both")

# filter widgets
date_from_lbl= tk.Label (filter_fr,text="date from:")
date_from_ENTRY = DateEntry ( filter_fr , width= 25 , date_pattern = "dd-mm-yyyy")
date_to_lbl= tk.Label (filter_fr,text="date to:")
date_to_ENTRY = DateEntry ( filter_fr , width= 25 , date_pattern = "dd-mm-yyyy")
flt_button_apply = tk.Button (filter_fr , width= 25, text= "Apply Filters" , command= filter_button_refresh)

date_from_ENTRY.set_date(flr_date_from)
date_to_ENTRY.set_date(flr_date_to)

# filter position
date_from_lbl.grid(row=0 , column=0 , padx= 2, pady = 5)
date_from_ENTRY.grid(row=0 , column=1 , padx= 2, pady = 5)
date_to_lbl.grid(row=0 , column=2 , padx= 2, pady = 5)
date_to_ENTRY.grid(row=0 , column=3 , padx= 2, pady = 5)
flt_button_apply.grid (row=0 , column=4 , padx= 2, pady = 5)

# =========================
# Content Frame
# =========================
basic_fr= tk.Frame (dashboard_fr, width=1200 , height=500,bg= "black")
basic_fr.pack_propagate(False)
basic_fr.pack(fill= "both", expand=True)

# =========================
# Overview Frame
# =========================

overview_fr= tk.Frame (basic_fr, width=1200 , height=500)
overview_fr.grid_propagate(False)
overview_fr.grid(row=0, column=0, sticky="nsew")
overview_fr.columnconfigure(0,weight=3,uniform="group1")
overview_fr.columnconfigure(1,weight=1,uniform="group1")
overview_fr.columnconfigure(2,weight=1,uniform="group1")
overview_fr.rowconfigure(0, weight=1)
overview_fr.tkraise()

left_side_fr=tk.Frame(overview_fr)
left_side_fr.grid(row=0, rowspan=2 ,column=0, sticky="nsew")
left_side_fr.grid_rowconfigure(0, weight=1)
left_side_fr.grid_columnconfigure(0, weight=1)


left_table = ttk.Treeview (left_side_fr,columns=("Transaction","Type","Amount", "Date", "Category"), show="headings" )
left_table.heading("Transaction", text= "Transaction")
left_table.heading("Amount", text= "Amount" )
left_table.heading("Type", text= "Type" )
left_table.heading("Category", text= "Category" )
left_table.heading("Date", text= "Date" )


left_table.column("Transaction", stretch=True)
left_table.column("Amount", stretch=True)
left_table.column("Type", stretch=True)
left_table.column("Category", stretch=True)
left_table.column("Date", stretch=True)


scrollbar_y= ttk.Scrollbar (left_side_fr,orient="vertical", command= left_table.yview)
left_table.configure(yscrollcommand=scrollbar_y.set)
scrollbar_x=ttk.Scrollbar (left_side_fr,orient="horizontal", command= left_table.xview)
left_table.configure(xscrollcommand=scrollbar_x.set)
scrollbar_y.grid(row=0,column=1, sticky= "ns")
scrollbar_x.grid(row=1,column=0, sticky= "ew")

left_table.bind("<ButtonRelease-1>", left_click)
left_table.bind("<Button-3>", right_click)

right_click_menu = tk.Menu(overview_fr, tearoff=0)

right_click_menu.add_command(label="Edit", command=lambda: edit_item())
right_click_menu.add_command(label="Delete", command=lambda: delete_item())


for row in overview_transactions_list:
    left_table.insert("","end", values=row )

left_table.grid(row= 0 , column= 0 , sticky= "nsew")

# bar chart
top_right_side_fr=tk.Frame(overview_fr)
top_right_side_fr.grid(row=0, column = 1, columnspan=2, sticky="nsew")
top_right_side_fr.grid_rowconfigure(0, weight=1)
top_right_side_fr.grid_columnconfigure(0, weight=1)



btm_right_side_fr=tk.Frame(overview_fr, relief="ridge", bd=2)
btm_right_side_fr.grid(row=1, column=1, sticky="nsew",columnspan=2, padx=20, pady=20)
btm_right_side_fr.grid_columnconfigure(0, weight=1)
btm_right_side_fr.grid_columnconfigure(1, weight=1)
#transaction
transaction_name_vr = tk.StringVar()
transaction_type_vr= tk.StringVar()
transaction_amount_vr = tk.StringVar()
transaction_category_vr= tk.StringVar()


transaction_name_lbl = tk.Label(btm_right_side_fr,text= "Transaction:", width=30)
transaction_name_entry = tk.Entry (btm_right_side_fr, textvariable=transaction_name_vr, width=30)
transaction_type_lbl = tk.Label(btm_right_side_fr,text= "Type:",  width=30)
transaction_type_entry= ttk.Combobox (btm_right_side_fr,  textvariable=transaction_type_vr , width=27)
transaction_type_entry["values"]=transaction_type_list
transaction_type_entry.current()
transaction_amount_lbl = tk.Label(btm_right_side_fr,text= "Amount:",  width=30)
transaction_amount_entry = tk.Entry (btm_right_side_fr, textvariable=transaction_amount_vr, width=30)
transaction_date_lbl= tk.Label(btm_right_side_fr,text= "Date:",  width=30)
transaction_date_entry=DateEntry(btm_right_side_fr,width= 27, date_pattern = "dd-mm-yyyy")
transaction_category_lbl= tk.Label(btm_right_side_fr,text= "Category:", width=30)
transaction_category_entry= ttk.Combobox (btm_right_side_fr,  textvariable=transaction_category_vr , width=27)
transaction_category_entry["values"]=()
transaction_add_button=tk.Button(btm_right_side_fr, text= "Submit" , width=30 , command=add_transaction)

transaction_name_lbl.grid(row=0,column=0,sticky="nw", padx=5, pady=5)
transaction_name_entry.grid(row=0,column=1,sticky="ne", padx=5, pady=5)
transaction_type_lbl.grid(row=1,column=0,sticky="nw", padx=5, pady=5)
transaction_type_entry.grid (row=1,column=1,sticky="ne", padx=5, pady=5)
transaction_amount_lbl.grid(row=2,column=0,sticky="nw", padx=5, pady=5)
transaction_amount_entry.grid(row=2,column=1,sticky="ne", padx=5, pady=5)
transaction_date_lbl.grid(row=3,column=0,sticky="nw", padx=5, pady=5)
transaction_date_entry.grid(row=3,column=1,sticky="ne", padx=5, pady=5)
transaction_category_lbl.grid(row=4,column=0,sticky="nw", padx=5, pady=5)
transaction_category_entry.grid(row=4,column=1,sticky="ne", padx=5, pady=5)
transaction_add_button.grid(row=5,column=1,sticky="ne", padx=5, pady=5)


# =========================
# expenses Frame
# =========================

expenses_fr= tk.Frame (basic_fr, width=1200 , height=500 , bg="red")
expenses_fr.grid_propagate(False)
expenses_fr.grid(row=0, column=0, sticky="nsew")

expenses_fr.columnconfigure(0,weight=3,uniform="group1")
expenses_fr.columnconfigure(1,weight=1,uniform="group1")
expenses_fr.columnconfigure(2,weight=1,uniform="group1")
expenses_fr.rowconfigure(0, weight=1)
expenses_fr.rowconfigure(1, weight=1)



# =========================
# income Frame
# =========================
income_fr= tk.Frame (basic_fr, width=1200 , height=500 , bg="blue")
income_fr.grid_propagate(False)
income_fr.grid(row=0, column=0, sticky="nsew")
# =========================
# subscription Frame
# =========================
subscription_fr= tk.Frame (basic_fr, width=1200 , height=500 , bg="green")
subscription_fr.grid_propagate(False)
subscription_fr.grid(row=0, column=0, sticky="nsew")

show_overview()
main.mainloop()
