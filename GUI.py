import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import export_excel as exp
from tkcalendar import DateEntry
import Financial as be
import charts as chart
import datetime

showing_frame= None
user_ID_number=0
transaction_type_list = ["INCOME","EXPENSE"]
overview_transactions_list = []
flr_date_to_date= datetime.datetime.today().date()
flr_date_from_date= flr_date_to_date.replace(day=1)
flr_date_to = flr_date_to_date.strftime("%d-%m-%Y")
flr_date_from = flr_date_from_date.strftime("%d-%m-%Y")

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

def get_total_amount (userid, type_of_tr,date_from, date_to):
    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    total_amount=be.Transaction.getAllAmountByMemberIdFilterByTransactionType(userid, type_of_tr, iso_date_from, iso_date_to)
    return total_amount

def header_refresh ():
    global user_ID_number, flr_date_from, flr_date_to
    income_amount.configure(text= f"Income: {get_total_amount(user_ID_number,transaction_type_list[0], flr_date_from, flr_date_to):.2f}")
    expenses_amount.configure(text= f"Expenses: {get_total_amount(user_ID_number,transaction_type_list[1], flr_date_from, flr_date_to):.2f}")
    available_assets.configure(text= f"Available Assets : {be.Transaction.getTotalByMemberId(user_ID_number):.2f}")

def overview_refresh ():
    global user_ID_number, flr_date_from, flr_date_to
    if user_ID_number == 0:
        return

    header_refresh()
    transaction_form.collect_category_per_user(user_ID_number)
    transaction_table.collect_all_transactions_per_user(user_ID_number, flr_date_from, flr_date_to)
    chart.income_vrs_expenses(overview_fr.top_right_side_fr, user_ID_number,flr_date_from, flr_date_to)
    transaction_form.user_id = user_ID_number
    overview_button.configure(state="disabled")
    expenses_button.configure(state="normal")
    income_button.configure(state="normal")

def expenses_refresh ():
    global user_ID_number, flr_date_from, flr_date_to

    if user_ID_number == 0:
        return

    header_refresh()
    chart.expenses_pie_chart(expenses_fr.top_right_side_fr, user_ID_number, flr_date_from, flr_date_to, "EXPENSE")
    chart.daily_spend(expenses_fr.btm_right_side_fr,user_ID_number, flr_date_from, flr_date_to)
    expenses_table.collect_type_transaction_per_user(user_ID_number,transaction_type_list[1], flr_date_from, flr_date_to)
    overview_button.configure(state="normal")
    expenses_button.configure(state="disabled")
    income_button.configure(state="normal")

def income_refresh ():
    global user_ID_number, flr_date_from, flr_date_to

    if user_ID_number == 0:
        return

    header_refresh()
    chart.expenses_pie_chart(income_fr.top_right_side_fr, user_ID_number,flr_date_from, flr_date_to, "INCOME")
    income_table.collect_type_transaction_per_user(user_ID_number,transaction_type_list[0], flr_date_from, flr_date_to)
    recurring_transactions.collect_recurring_data(user_ID_number, flr_date_from, flr_date_to)
    overview_button.configure(state="normal")
    expenses_button.configure(state="normal")
    income_button.configure(state="disabled")

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
        show_overview()

    else:
        messagebox.showerror("Login Error", "Username or password is wrong.\nPlease try again.")
        username_label.configure(fg="red")
        password_label.configure(fg="red")

def show_overview():
    global showing_frame
    overview_fr.tkraise()
    overview_refresh()
    showing_frame = "overview"

def show_income():
    global showing_frame
    income_fr.tkraise()
    income_refresh()
    showing_frame = "income"

def show_expenses():
    global showing_frame
    expenses_fr.tkraise()
    expenses_refresh()
    showing_frame = "expenses"

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
    global flr_date_from , flr_date_to ,user_ID_number,showing_frame
    flr_date_from = date_from_ENTRY.get()
    flr_date_to = date_to_ENTRY.get()
    if showing_frame == "overview":
        overview_refresh()
    elif showing_frame == "expenses":
        expenses_refresh()
    elif showing_frame == "income":
        income_refresh()

def export_data (user_id,date_from, date_to ):
    filter_button_refresh()
    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    saved_file_path =filedialog.asksaveasfilename( defaultextension=".xlsx",filetypes=[("Excel files", "*.xlsx")],title="Save Export As",initialfile=f"export_{date_from}_to_{date_to}.xlsx" )

    exp.export_to_excel(user_id,iso_date_from,iso_date_to, filename=saved_file_path)
    messagebox.showinfo("Export", "File saved successfully!")

def new_transaction_window ():
    global user_ID_number
    pop_up = tk.Toplevel(main)
    pop_up.geometry("350x300")
    pop_up.title ("Add transaction")
    form_widget = Transaction_form(pop_up, on_submit=add_transaction, user_id=user_ID_number,on_close=pop_up.destroy)
    form_widget.grid(row=0, column=0, sticky="nsew")
    form_widget.collect_category_per_user(user_ID_number)

def add_new_category (category_name):
    global user_ID_number
    new_name = category_name
    new_category=be.Category(new_name,user_ID_number)
    new_category.createCategoryByMemberId(user_ID_number)
    filter_button_refresh()

def delete_validation (name_var):
    if name_var not in transaction_form.category_list:
        messagebox.showerror("Error", "Please select a category.")
    else:
        be.Category.deleteCategoryByCategoryId(transaction_form.category_map_name_id[name_var])
        filter_button_refresh()

def delete_category ():
    global user_ID_number
    pop_up_category = tk.Toplevel (main)
    pop_up_category.geometry("350x70")
    pop_up_category.title("Delete Category")
    filter_button_refresh()
    name_var = tk.StringVar()
    tk.Label(pop_up_category, text="Category:", width=15).grid(row=0, column=0, padx=5, pady=5)
    ttk.Combobox(pop_up_category, textvariable=name_var, width=25, values=transaction_form.category_list).grid(row=0, column=1, padx=5,pady=5)
    tk.Button(pop_up_category, text="Submit",command=lambda: [delete_validation(name_var.get()), pop_up_category.destroy()]).grid(row=1, column=1,pady=5)

def new_category_window():
    pop_up_category = tk.Toplevel (main)
    pop_up_category.geometry("250x70")
    pop_up_category.title("New Category")
    name_var = tk.StringVar()

    tk.Label(pop_up_category, text="Category Name:").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(pop_up_category, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(pop_up_category, text="Submit", command=lambda: [add_new_category(name_var.get()),pop_up_category.destroy()]).grid(row=1, column=1, pady=5)

def on_income_select():
    income_fr.delete_button.configure(state="normal")
    income_fr.edit_button.configure(state="normal")

def on_overview_select():
    overview_fr.delete_button.configure(state="normal")
    overview_fr.edit_button.configure(state="normal")

def on_expenses_select():
    expenses_fr.delete_button.configure(state="normal")
    expenses_fr.edit_button.configure(state="normal")

# =========================
#Classes
# =========================

class Basic_navigation_frm(tk.Frame):
    def __init__(self, parent,table=None):
        super().__init__(parent)
        self.table = table
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
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
        self.left_side_fr.grid_rowconfigure(0, weight=15)
        self.left_side_fr.grid_rowconfigure(1, weight=1)
        self.left_side_fr.grid_columnconfigure(0, weight=1)
        self.left_side_fr.grid_columnconfigure(1, weight=1)
        self.left_side_fr.grid_columnconfigure(2, weight=1)
        self.left_side_fr.grid_columnconfigure(3, weight=1)
        self.left_side_fr.grid_columnconfigure(4, weight=10)
        self.delete_button = tk.Button (self.left_side_fr,text= "Delete Transaction",width= 25, anchor= "w",command=lambda: self.table.delete_item() if self.table else None,state="disabled")
        self.edit_button = tk.Button(self.left_side_fr,text="Edit Transaction",width= 25, anchor= "w", command=lambda: self.table.edit_item() if self.table else None, state="disabled")
        self.ad_category_button = tk.Button(self.left_side_fr,text="Add New Category",width= 25, anchor= "w", command= new_category_window)
        self.delete_category_button = tk.Button(self.left_side_fr, text="Delete Category", width=25, anchor="w",command=delete_category)
        self.delete_button.grid (row=1, column=3, padx=2, pady=2)
        self.edit_button.grid (row=1, column=2, padx=2, pady=2)
        self.ad_category_button.grid (row=1, column=0, padx=2, pady=2)
        self.delete_category_button.grid (row=1, column=1, padx=2, pady=2)

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
    def __init__(self, parent, on_select=None):
        super().__init__(parent)
        self.on_select = on_select
        self.left_table = ttk.Treeview(self, columns=("ID","Transaction", "Type", "Amount", "Date", "Category","Recurring"), show="headings")
        for  column in self.left_table["columns"]:
            self.left_table.heading(column, text = column)
            self.left_table.column(column,stretch=True)
        self.left_table.column("ID", width=0, stretch=False)
        self.left_table.heading("ID", text="")

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
        self.transactions_data.extend(be.Transaction.getAllTransactionsByMemberId(user_id, iso_date_from, iso_date_to))
        self.transactions_data = [ (t[0], t[1], t[2], t[3], datetime.datetime.strptime(t[4], "%Y-%m-%d").strftime("%d-%m-%Y"), t[7],t[5])for t in sorted(self.transactions_data,key=lambda x: x[4],reverse=True)]
        self.load_data()

    def collect_type_transaction_per_user (self, user_id, choose_type,date_from, date_to):
        self.transactions_data.clear()
        iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
        iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
        self.transactions_data.extend(be.Transaction.getAllTransactionsByMemberIdFilterByType(user_id, choose_type, iso_date_from, iso_date_to))
        self.transactions_data = [(t[0],t[1], t[2], t[3], datetime.datetime.strptime(t[4], "%Y-%m-%d").strftime("%d-%m-%Y"), t[7],t[5]) for t in sorted(self.transactions_data, key=lambda x: x[4], reverse=True)]
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
            self.selected_item_from_table = item
            self.selected_values_from_table = self.left_table.item(item, "values")
            if self.on_select:
                self.on_select()

    def right_click(self,event):
        self.selected_item_from_table = self.left_table.identify_row(event.y)
        if not self.selected_item_from_table:
            return

        self.left_table.selection_set(self.selected_item_from_table)
        self.selected_values_from_table = self.left_table.item(self.selected_item_from_table, "values")
        self.right_click_menu.post(event.x_root, event.y_root)
        if self.on_select:
            self.on_select()

    def delete_item(self):
        pop_up = tk.Toplevel (self)
        pop_up.geometry("250x100")
        pop_up.title("DELETE TRANSACTION")

        tk.Label(pop_up, text="Are you sure you want to delete transaction:\n" + self.selected_values_from_table[1]).grid(row=0, column=0,columnspan=2, padx=5, pady=5)
        tk.Button(pop_up, text="Submit",command=lambda: [be.Transaction.deleteTransactionByTransactionId(self.selected_values_from_table[0]), pop_up.destroy(),filter_button_refresh()]).grid(row=1, column=0, pady=5)
        tk.Button(pop_up, text="Cancel",command=lambda: pop_up.destroy()).grid(row=1, column=1, pady=5)

    def edit_item(self):
        pop_up = tk.Toplevel(self )
        pop_up.geometry("400x300")
        pop_up.title("UPDATE TRANSACTION")
        form=Transaction_form (pop_up, on_submit=add_transaction,user_id=user_ID_number,on_close=pop_up.destroy,transaction_id=self.selected_values_from_table[0])
        form.grid(row=0, column=0, sticky="nsew")
        form.collect_category_per_user(user_ID_number)
        form.autopopulate_form(self.selected_values_from_table)

class Transaction_form (tk.Frame):
    def __init__(self, parent,on_submit,user_id,on_close=None, transaction_id=None):
        super().__init__(parent)

        self.on_close = on_close
        self.transaction_id = transaction_id
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

        self.transaction_title_label = tk.Label(self, text="Add New Transaction", font=("arial", 14, "bold"), anchor="center")
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

        self.transaction_title_label.grid (row=0, column=0, sticky="nsew", padx=2, pady=15 , columnspan= 2)
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
            if self.transaction_id:
                data_list = be.Transaction( data["name"],data["type"],data["amount"],data["date"], data["category_id"],data["recurring"])
                be.Transaction.UpdateTransactionByTransactionId(self.transaction_id, data_list)
                filter_button_refresh()
            else:
                self.on_submit(data)
                self.transaction_amount_vr.set("")
                self.transaction_name_vr.set("")
                self.transaction_category_vr.set("")
                self.transaction_type_vr.set("")
                self.transaction_date_entry.set_date(datetime.date.today())
            if self.on_close:
                self.on_close()


    def number_validation(self, value):
        try:
            amount_valid = float(value)

            if amount_valid >= 0:
                return True
            else:
                return False

        except ValueError:
            return False

    def autopopulate_form (self,transaction_data):
        self.transaction_name_vr.set(transaction_data[1])
        self.transaction_type_vr.set(transaction_data [2])
        self.transaction_amount_vr.set(transaction_data [3])
        self.transaction_category_vr.set(transaction_data [5])
        self.transaction_date_entry.set_date(datetime.datetime.strptime(transaction_data[4],"%d-%m-%Y").date())
        self.is_recurring.set(transaction_data[6])

class Recurring_transactions (tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.recurring_table = ttk.Treeview(self, columns=("Transaction", "Type", "Amount", "Next Transaction Date", "Category"), show="headings")
        for  column in self.recurring_table["columns"]:
            self.recurring_table.heading(column, text = column)
            self.recurring_table.column(column, stretch=True)
        self.recurring_title  = tk.Label(self, text = "Recurring Transactions" , font=( "arial",16,"bold") )


        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.recurring_table.yview)
        self.recurring_table.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.recurring_table.xview)
        self.recurring_table.configure(xscrollcommand=self.scrollbar_x.set)

        self.recurring_table.grid(row=1, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.scrollbar_x.grid(row=2, column=0, sticky="ew" , pady= 2)
        self.recurring_title.grid(row=0, column=0, sticky="nsew", padx= 5, pady=5)


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.recurring_data = []

    def collect_recurring_data(self,user_id, date_from, date_to):
        self.recurring_data.clear()
        iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
        iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
        self.recurring_data.extend(be.Transaction.getAllSubscriptionsByMemberIdFilterRecurring(user_id, iso_date_from, iso_date_to))
        print("des to table gia " + str(self.recurring_data))
        self.recurring_data = [( t[1], t[2], t[3], datetime.datetime.strptime(t[4], "%Y-%m-%d").strftime("%d-%m-%Y"), t[7]) for t in sorted(self.recurring_data,key=lambda x: x[4],reverse=False)]
        for item in self.recurring_table.get_children():
            self.recurring_table.delete(item)
        for single_row in self.recurring_data:
            self.recurring_table.insert("", "end", values=single_row)

# =========================
# Main Window
# =========================

main= tk.Tk()
main.title("Family Finance Manager")
main.geometry ("400x200")
main.resizable(False,False)

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
header_fr.columnconfigure (0 , weight=1)
header_fr.columnconfigure (1 , weight=1)
header_fr.columnconfigure (2 , weight=1)
header_fr.columnconfigure (3 , weight=1)
header_fr.columnconfigure (4 , weight=2)

# header widgets
name_lbl = tk.Label(header_fr, text= "Name: Will retrieve auto", width= 30, anchor= "w", relief="groove")
username_lbl = tk.Label(header_fr, text= "Username: Will retrieve auto", width= 30, anchor= "w", relief="groove")
income_amount = tk.Label(header_fr, text= "Income:" , width= 30, anchor= "w", relief="groove")
expenses_amount = tk.Label(header_fr, text= "Expenses:" , width= 30, anchor= "w", relief="groove")
overview_button = tk.Button (header_fr, text= "Overview",width= 30, anchor= "w", command= show_overview )
expenses_button = tk.Button (header_fr, text= "Expenses",width= 30, anchor= "w", command=show_expenses)
income_button = tk.Button (header_fr, text= "Income",width= 30, anchor= "w" , command= show_income)
new_transaction_button = tk.Button (header_fr, text= "Add Transaction",width= 30, anchor= "w", command= new_transaction_window)
available_assets= tk.Label(header_fr , text= "Available Assets :" + str(be.Transaction.getTotalByMemberId(user_ID_number)),font=("arial", 16),relief="ridge", bd=5,width= 30 )

# header position
name_lbl.grid (row= 0 , column= 0 , padx=5 , pady= 5, sticky="w")
username_lbl.grid (row= 0 , column= 1 , padx=5 , pady= 5, sticky="w")
income_amount.grid (row= 0 , column= 2 , padx=5 , pady= 5, sticky="w")
expenses_amount.grid (row= 0 , column= 3 , padx=5 , pady= 5, sticky="w")
overview_button.grid (row= 1 , column= 0 , padx=5 , pady= 5, sticky="w")
expenses_button.grid (row= 1 , column= 1 , padx=5 , pady= 5, sticky="w")
income_button.grid (row= 1 , column= 2 , padx=5 , pady= 5, sticky="w")
new_transaction_button.grid (row= 1 , column= 3 , padx=5 , pady= 5, sticky="w")
available_assets.grid (row= 0 , column= 4 ,rowspan=2, padx=5 , pady= 5, sticky="w")
# filter frame

filter_fr = tk.Frame(dashboard_fr, width=1400 , height=50)
filter_fr.pack_propagate(False)
filter_fr.pack (fill= "both")

# filter widgets
date_from_lbl= tk.Label (filter_fr,text="Date from:")
date_from_ENTRY = DateEntry ( filter_fr , width= 25 , date_pattern = "dd-mm-yyyy")
date_to_lbl= tk.Label (filter_fr,text="Date to:")
date_to_ENTRY = DateEntry ( filter_fr , width= 25 , date_pattern = "dd-mm-yyyy")
flt_button_apply = tk.Button (filter_fr , width= 30, text= "Apply Filters" , command= filter_button_refresh)
export_button = tk.Button (filter_fr, text= "Export", width= 30, command=lambda:export_data(user_ID_number,flr_date_from,flr_date_to))

date_to_ENTRY.set_date(flr_date_to_date)
date_from_ENTRY.set_date(flr_date_from_date)

# filter position
date_from_lbl.grid(row=0 , column=0 , padx= 2, pady = 5)
date_from_ENTRY.grid(row=0 , column=1 , padx= 2, pady = 5)
date_to_lbl.grid(row=0 , column=2 , padx= 2, pady = 5)
date_to_ENTRY.grid(row=0 , column=3 , padx= 2, pady = 5)
flt_button_apply.grid (row=0 , column=4 , padx=5, pady = 5)
export_button.grid (row= 0 , column= 5 , padx=5 , pady = 5)


# =========================
# Content Frame
# =========================

basic_fr= tk.Frame (dashboard_fr, width=1400 , height=650,bg= "black")
basic_fr.pack_propagate(False)
basic_fr.pack(fill= "both", expand=True)
basic_fr.grid_rowconfigure(0, weight=1)
basic_fr.grid_columnconfigure(0, weight=1)

# =========================
# Overview Frame
# =========================

overview_fr= Basic_navigation_frm (basic_fr)
overview_fr.grid_propagate(False)
overview_fr.grid(row=0, column=0, sticky="nsew")

transaction_table = Show_transactions(overview_fr.left_side_fr,on_select=on_overview_select)
transaction_table.grid(row= 0 , column= 0 , columnspan= 4, sticky= "nsew")
overview_fr.table = transaction_table
transaction_form = Transaction_form (overview_fr.btm_right_side_fr,on_submit=add_transaction ,user_id=user_ID_number)
transaction_form.grid(row= 0 , column= 0 , sticky= "nsew")


# =========================
# expenses Frame
# =========================

expenses_fr= Basic_navigation_frm (basic_fr)
expenses_fr.grid_propagate(False)
expenses_fr.grid(row=0, column=0, sticky="nsew")


expenses_table = Show_transactions(expenses_fr.left_side_fr,on_select=on_expenses_select)
expenses_table.grid(row= 0 , column= 0 ,columnspan= 4, sticky= "nsew")
expenses_fr.table = expenses_table

# =========================
# income Frame
# =========================
income_fr= Basic_navigation_frm (basic_fr)
income_fr.grid_propagate(False)
income_fr.grid(row=0, column=0, sticky="nsew")

income_table = Show_transactions(income_fr.left_side_fr,on_select=on_income_select)
income_table.grid(row= 0 , column= 0 ,columnspan= 4, sticky= "nsew")
income_fr.table = income_table

recurring_transactions = Recurring_transactions(income_fr.btm_right_side_fr)
recurring_transactions.grid(row= 0 , column= 0 , sticky= "nsew")

main.mainloop()
