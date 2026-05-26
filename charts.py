import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Financial as be
import matplotlib.ticker as ticker
import datetime

# =========================
# Pie chart
# =========================

def expenses_pie_chart (frame,user_id,date_from, date_to):
    for widget in frame.winfo_children():
        widget.destroy()


    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")

    all_expenses_transactions = be.Transaction.getAllTransactionsByMemberIdFilterByType(user_id,"EXPENSE",iso_date_from, iso_date_to)
    total_amount_per_category={}
    for name,amount,date,categories in all_expenses_transactions:
        if categories in total_amount_per_category:
            total_amount_per_category[categories] += amount
        else:
            total_amount_per_category[categories]=amount
    total_amount_per_category = dict(sorted(total_amount_per_category.items(), key=lambda x: x[1], reverse=True))
    totals_amount = list(total_amount_per_category.values())
    unique_categories = list (total_amount_per_category.keys())

    fig, ax =plt.subplots(figsize=(6, 3))
    fig.subplots_adjust(left=0.05, right=0.5, top=0.8, bottom=0)
    ax.pie (totals_amount , labels= None  , startangle= 215 , autopct='%1.1f%%' ,pctdistance= 1.3 , radius= 0.9)
    ax.set_title("Expenses by Category")
    ax.legend (unique_categories, loc = "lower left" , bbox_to_anchor=(1,0))

    canvas = FigureCanvasTkAgg(fig, master= frame )
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(row=0, column=0, columnspan= 2 , sticky="nsew")
    plt.close(fig)

# =========================
# Bar chart
# =========================

def income_vrs_expenses(frame,user_id,date_from, date_to):
    for widget in frame.winfo_children():
        widget.destroy()

    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    total_income= be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_id,"INCOME",iso_date_from, iso_date_to)
    total_expenses=be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_id,"EXPENSE",iso_date_from, iso_date_to)


    money_type= ["Expenses","Income"]
    total_value = [round(total_expenses,2), round(total_income,2 )]

    fig,ax=plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.2, right=0.9)


    bars= ax.barh(money_type,total_value, color= ["red" , "green"])

    for i, bar in enumerate(bars):
        width = bar.get_width()

        ax.text( width / 2, bar.get_y() + bar.get_height() / 2, str(total_value[i]) + " €", ha='center', va='center', color='white', fontweight='bold' )
    ax.set_title ("Income - Expenses")


    canvas = FigureCanvasTkAgg(fig, master= frame )
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(columnspan=2 )
    plt.close(fig)


# =========================
# Line chart
# =========================

def daily_spend (frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # fake data to use is to many
    days = [
            "2026-03-01","2026-03-02","2026-03-03","2026-03-04","2026-03-05","2026-03-06","2026-03-07",
            "2026-03-08","2026-03-09","2026-03-10","2026-03-11","2026-03-12","2026-03-13","2026-03-14",
            "2026-03-15","2026-03-16","2026-03-17","2026-03-18","2026-03-19","2026-03-20","2026-03-21",
            "2026-03-22","2026-03-23","2026-03-24","2026-03-25","2026-03-26","2026-03-27","2026-03-28",
            "2026-03-29","2026-03-30","2026-03-31"]
    amount_spend = [120.4, 54.2, 67.8, 57.9, 162.3, 24.3, 110.4,
                    72.0, 23.5, 108.2, 65.9, 117.0, 41.9, 132.6,
                    88.2, 143.3, 58.7, 125.4, 38.6, 150.2, 97.8,
                    170.0, 89.5, 78.9, 55.0, 112.4, 96.3, 140.2,
                    60.1, 75.4, 190.0]

    fig,ax=plt.subplots(figsize=(9, 3))
    ax.plot (days,amount_spend , color= "black" )
    fig.subplots_adjust( left=0.1,right=0.9,top=0.9,bottom=0.25)
    ax.set_title("Daily Spend")
    ax.tick_params(axis='x', labelrotation=45, labelsize=6)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))

    canvas = FigureCanvasTkAgg(fig, master= frame )
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(row=0, column=0, sticky="nsew")
    plt.close(fig)
