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

def overview_refresh ():
    global user_ID_number

    if user_ID_number == 0:
        return

    income_amount.configure(text= "Income: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"INCOME", None, None)))
    expenses_amount.configure(text= "Expenses: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"EXPENSE", None, None)))
    transaction_form.collect_category_per_user(user_ID_number)
    transaction_table.collect_all_transactions_per_user(user_ID_number, flr_date_from, flr_date_to)
    chart.income_vrs_expenses(overview_fr.top_right_side_fr, user_ID_number)
    transaction_form.user_id = user_ID_number

def expenses_refresh ():
    global user_ID_number

    if user_ID_number == 0:
        return

    income_amount.configure(text= "Income: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"INCOME", None, None)))
    expenses_amount.configure(text= "Expenses: " + str(be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_ID_number,"EXPENSE", None, None)))
    transaction_form.collect_category_per_user(user_ID_number)
    #transaction_table.collect_type_transaction_per_user(user_ID_number , choose_type= "EXPENSE")
    chart.expenses_pie_chart(expenses_fr.top_right_side_fr, user_ID_number)
    transaction_form.user_id = user_ID_number
    chart.daily_spend(expenses_fr.btm_right_side_fr)
    transaction_table.collect_all_transactions_per_user(user_ID_number, flr_date_from, flr_date_to) # to be removed

def show_dashboard():

    if be.Member.validateMember(username_added.get(),password_added.get()):
        user_information = be.Member.getMemberByUsername(username_added.get())
        global user_ID_number
        user_ID_number= user_information[0]
        login_fr.pack_forget()
        main.geometry("1400x750")
        main.minsize(1400, 750)
        dashboard_fr.pack(fill="both", expand=True)
        name_lbl.configure(text="Name: "+ user_information[1] + " " + user_information[2])
        username_lbl.configure(text= "Username: " + user_information[3] )
        overview_refresh()

    else:
        messagebox.showerror("Login Error", "Username or password is wrong.\nPlease try again.")
        username_label.configure(fg="red")
        password_label.configure(fg="red")


def show_overview():
    overview_fr.tkraise()
    overview_refresh()

def show_income():
    income_fr.tkraise()

def show_expenses():
    expenses_fr.tkraise()
    expenses_refresh()

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


def add_transaction(data):

        new_transaction=be.Transaction(data["name"],data["type"],data["amount"], data["date"],data["category_id"] ,data ["recurring"])
        new_transaction.createTransactionByCategoryId(data["category_id"])
        overview_refresh()



def filter_button_refresh ():
    global flr_date_from , flr_date_to
    flr_date_from = date_from_ENTRY.get()
    flr_date_to = date_to_ENTRY.get()
    transaction_table.collect_all_transactions_per_user(user_ID_number,flr_date_from,flr_date_to)


# =========================
#Classes
# =========================

class Basic_navigation_frm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # basic frame of screen

        self.overview_fr = tk.Frame(self, width=1400, height=650)
        self.overview_fr.grid_propagate(False)
        self.overview_fr.grid(row=0, column=0, sticky="nsew")
        self.overview_fr.columnconfigure(0, weight=2, uniform="group1")
        self.overview_fr.columnconfigure(1, weight=1, uniform="group1")
        self.overview_fr.rowconfigure(0, weight=1)
        self.overview_fr.rowconfigure(1, weight=1)
        self.overview_fr.tkraise()

        # left side frame

        self.left_side_fr = tk.Frame(self.overview_fr)
        self.left_side_fr.grid(row=0, rowspan=2, column=0, sticky="nsew")
        self.left_side_fr.grid_rowconfigure(0, weight=5)
        self.left_side_fr.grid_rowconfigure(1, weight=1)
        self.left_side_fr.grid_columnconfigure(0, weight=1)

        #upper right frame

        self.top_right_side_fr = tk.Frame(self.overview_fr, relief="ridge", bd=2)
        self.top_right_side_fr.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.top_right_side_fr.grid_rowconfigure(0, weight=1)
        self.top_right_side_fr.grid_columnconfigure(0, weight=1)


        # lower right frame

        self.btm_right_side_fr = tk.Frame(self.overview_fr, relief="ridge", bd=2)
        self.btm_right_side_fr.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        self.btm_right_side_fr.grid_columnconfigure(0, weight=1)
        self.btm_right_side_fr.grid_columnconfigure(1, weight=1)

class Show_transactions (tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.left_table = ttk.Treeview(self, columns=("Transaction", "Type", "Amount", "Date", "Category"), show="headings")
        for  column in self.left_table["columns"]:
            self.left_table.heading(column, text = column)
            self.left_table.column(column,stretch=True)

        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.left_table.yview)
        self.left_table.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.left_table.xview)
        self.left_table.configure(xscrollcommand=self.scrollbar_x.set)

        self.left_table.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew" , pady= 2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.left_table.bind("<ButtonRelease-1>", self.left_click)
        self.left_table.bind("<Button-3>", self.right_click)

        self.right_click_menu = tk.Menu(self, tearoff=0)

        self.right_click_menu.add_command(label="Edit", command = self.edit_item)
        self.right_click_menu.add_command(label="Delete", command = self.delete_item)

        self.transactions_data = []
        self.selected_item_from_table = None
        self.selected_values_from_table = None

    def collect_all_transactions_per_user(self,user_id, date_from, date_to):
        self.transactions_data.clear()
        iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
        iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
        self.transactions_data.extend(be.Transaction.getAllTransactionsByMemberIdFilterDate(user_id, iso_date_from, iso_date_to))
        self.transactions_data = [(t[0], t[1], t[2], datetime.datetime.strptime(t[3], "%Y-%m-%d").strftime("%d-%m-%Y"), t[4]) for t in self.transactions_data]
        self.load_data()

    def collect_type_transaction_per_user (self, user_id, choose_type): # need to add the dates once the function is ready
        self.transactions_data.clear()
        #iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")     will be added later
        #iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")         will be added later
        self.transactions_data.extend(be.Transaction.getAllTransactionsByMemberIdFilterByType(user_id, choose_type, None, None))
        self.transactions_data = [(t[0], t[1], t[2], datetime.datetime.strptime(t[3], "%Y-%m-%d").strftime("%d-%m-%Y"), t[4]) for t in self.transactions_data]
        self.load_data()


    def load_data (self):
        for item in self.left_table.get_children():
            self.left_table.delete(item)
        for single_row in self.transactions_data:
            self.left_table.insert("", "end", values=single_row)

    def left_click(self,event):
        item = self.left_table.identify_row(event.y)
        if item:
            self.left_table.selection_set(item)

    def right_click(self,event):
        self.selected_item_from_table = self.left_table.identify_row(event.y)
        if not self.selected_item_from_table:
            return

        self.left_table.selection_set(self.selected_item_from_table)
        self.selected_values_from_table = self.left_table.item(self.selected_item_from_table, "values")
        self.right_click_menu.post(event.x_root, event.y_root)

    def delete_item(self):
        print(self.selected_values_from_table)

    def edit_item(self):
        pass

class Transaction_form (tk.Frame):
    def __init__(self, parent,on_submit,user_id):
        super().__init__(parent)

        self.user_id = user_id
        self.on_submit = on_submit
        self.transaction_name_vr = tk.StringVar()
        self.transaction_type_vr = tk.StringVar()
        self.transaction_amount_vr = tk.StringVar()
        self.transaction_category_vr = tk.StringVar()
        self.transaction_type_list = ["INCOME","EXPENSE"]
        self.transaction_recurring_list = ["YES", "NO"]
        self.category_map_name_id = {}
        self.category_map_id_name = {}
        self.category_list = []
        self.is_recurring = tk.StringVar(value="NO")

        self.transaction_title_label = tk.Label(register_fr, text="Add New Transaction", font=("arial", 14, "bold"), padx=5, pady=5)
        self.transaction_name_lbl = tk.Label(self, text="Transaction:", width=15)
        self.transaction_name_entry = tk.Entry(self, textvariable=self.transaction_name_vr, width=30)
        self.transaction_type_lbl = tk.Label(self, text="Type:", width=15)
        self.transaction_type_entry = ttk.Combobox(self, textvariable=self.transaction_type_vr, width=27)
        self.transaction_type_entry["values"] = self.transaction_type_list
        self.transaction_type_entry.current(0)
        self.transaction_amount_lbl = tk.Label(self, text="Amount:", width=15)
        self.transaction_amount_entry = tk.Entry(self, textvariable=self.transaction_amount_vr, width=30)
        self.transaction_date_lbl = tk.Label(self, text="Date:", width=15)
        self.transaction_date_entry = DateEntry(self, width=27, date_pattern="dd-mm-yyyy")
        self.transaction_category_lbl = tk.Label(self, text="Category:", width=15)
        self.transaction_category_entry = ttk.Combobox(self, textvariable=self.transaction_category_vr, width=27)
        self.transaction_category_entry["values"] = ()
        self.transaction_add_button = tk.Button(self, text="Submit", width=30,command=self.add_transaction)
        self.is_recurring_lbl = tk.Label(self, text="Monthly recurring: ", width=15)
        self.is_recurring_checkbox =tk.Checkbutton (self,text= "YES" , variable=self.is_recurring, onvalue= "YES" , offvalue= "NO" )

        self.transaction_title_label.grid (row=0, column=0, sticky="nsew", padx=2, pady=5 , columnspan= 2)
        self.transaction_name_lbl.grid(row=1, column=0, sticky="nw", padx=2, pady=5)
        self.transaction_name_entry.grid(row=1, column=1, sticky="ne", padx=2, pady=5)
        self.transaction_type_lbl.grid(row=2, column=0, sticky="nw", padx=2, pady=5)
        self.transaction_type_entry.grid(row=2, column=1, sticky="ne", padx=2, pady=5)
        self.transaction_amount_lbl.grid(row=3, column=0, sticky="nw", padx=2, pady=5)
        self.transaction_amount_entry.grid(row=3, column=1, sticky="ne", padx=2, pady=5)
        self.transaction_date_lbl.grid(row=4, column=0, sticky="nw", padx=2, pady=5)
        self.transaction_date_entry.grid(row=4, column=1, sticky="ne", padx=2, pady=5)
        self.transaction_category_lbl.grid(row=5, column=0, sticky="nw", padx=2, pady=5)
        self.transaction_category_entry.grid(row=5, column=1, sticky="ne", padx=2, pady=5)
        self.is_recurring_lbl.grid(row=6, column=0, sticky="nw", padx=2, pady=5)
        self.is_recurring_checkbox.grid(row=6, column=1, padx=2, pady=5)
        self.transaction_add_button.grid(row=7, column=1, sticky="ne", padx=2, pady=5)

    def collect_category_per_user(self,user_id):
        self.category_list.clear()
        full_list = be.Category.getAllCategoriesByMemberId(user_id)
        for category_id, category_name, member_id in full_list:
            self.category_map_name_id[category_name] = category_id
            self.category_map_id_name[category_id] = category_name
            self.category_list.append(category_name)
        self.transaction_category_entry["values"] = self.category_list

    def add_transaction(self):
        if self.transaction_name_vr.get().strip() == "" or self.transaction_type_vr.get().strip() == "" or self.transaction_amount_vr.get().strip() == "" or self.transaction_category_vr.get().strip() == "" or self.transaction_category_entry.get() not in self.category_list or self.transaction_type_entry.get() not in self.transaction_type_list:
            messagebox.showerror("Empty Fields", "Please add all the required fields.")
            self.transaction_amount_lbl.configure(fg="red")
            self.transaction_name_lbl.configure(fg="red")
            self.transaction_category_lbl.configure(fg="red")
            self.transaction_type_lbl.configure(fg="red")
        elif not self.number_validation(self.transaction_amount_vr.get()):
            messagebox.showerror("Wrong Amount", "Please ensure you add a valid amount.\nEx:5.76")
            self.transaction_amount_lbl.configure(fg="red")
            self.transaction_name_lbl.configure(fg="black")
            self.transaction_category_lbl.configure(fg="black")
            self.transaction_type_lbl.configure(fg="black")
        else:
            self.transaction_amount_lbl.configure(fg="black")
            self.transaction_name_lbl.configure(fg="black")
            self.transaction_category_lbl.configure(fg="black")
            self.transaction_type_lbl.configure(fg="black")
            selected_category_id = self.category_map_name_id[self.transaction_category_vr.get()]
            iso_date = datetime.datetime.strptime(self.transaction_date_entry.get(), "%d-%m-%Y").date().isoformat()
            data = {"name": self.transaction_name_vr.get(), "type": self.transaction_type_vr.get() , "amount": self.transaction_amount_vr.get() , "date": iso_date, "category_id": selected_category_id, "recurring": self.is_recurring.get()}
            self.on_submit(data)
            self.transaction_amount_vr.set("")
            self.transaction_name_vr.set("")
            self.transaction_category_vr.set("")
            self.transaction_type_vr.set("")
            self.transaction_date_entry.set_date(datetime.date.today())

    def number_validation(self, value):  # use to check the number is positive float
        try:
            amount_valid = float(value)

            if amount_valid >= 0:
                return True
            else:
                return False

        except ValueError:
            return False



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
header_fr = tk.Frame (dashboard_fr, height=50 , width=1400)
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

filter_fr = tk.Frame(dashboard_fr, width=1400 , height=50)
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
basic_fr= tk.Frame (dashboard_fr, width=1400 , height=650,bg= "black")
basic_fr.pack_propagate(False)
basic_fr.pack(fill= "both", expand=True)

# =========================
# Overview Frame
# =========================

overview_fr= Basic_navigation_frm (basic_fr)
overview_fr.grid_propagate(False)
overview_fr.grid(row=0, column=0, sticky="nsew")


transaction_table = Show_transactions(overview_fr.left_side_fr)
transaction_table.grid(row= 0 , column= 0 , sticky= "nsew")

transaction_form = Transaction_form (overview_fr.btm_right_side_fr,on_submit=add_transaction ,user_id=user_ID_number)
transaction_form.grid(row= 0 , column= 0 , sticky= "nsew")


# =========================
# expenses Frame
# =========================



expenses_fr= Basic_navigation_frm (basic_fr)
expenses_fr.grid_propagate(False)
expenses_fr.grid(row=0, column=0, sticky="nsew")

expenses_table = Show_transactions(expenses_fr.left_side_fr)
expenses_table.grid(row= 0 , column= 0 , sticky= "nsew")



# =========================
# income Frame
# =========================
income_fr= tk.Frame (basic_fr, width=1400 , height=650 , bg="blue")
income_fr.grid_propagate(False)
income_fr.grid(row=0, column=0, sticky="nsew")
# =========================
# subscription Frame
# =========================
subscription_fr= tk.Frame (basic_fr, width=1400 , height=650 , bg="green")
subscription_fr.grid_propagate(False)
subscription_fr.grid(row=0, column=0, sticky="nsew")

show_overview()
main.mainloop()
