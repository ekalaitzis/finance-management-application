import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Financial as be
import matplotlib.ticker as ticker
import datetime

# =========================
# Pie chart
# =========================

def expenses_pie_chart (frame,user_id,date_from, date_to, trans_type):
    for widget in frame.winfo_children():
        widget.destroy()


    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    print("pie chart chart dates from " + iso_date_from + "to " + iso_date_to)
    total_amount_per_category=be.Transaction.getAllTransactionsByMemberIdGroupedByCategory(user_id,trans_type,iso_date_from, iso_date_to)

    totals_amount = [column [2] for column in total_amount_per_category ]
    unique_categories = [column [1] for column in total_amount_per_category ]


    fig, ax =plt.subplots(figsize=(6, 3))
    fig.subplots_adjust(left=0.05, right=0.5, top=0.8, bottom=0)
    ax.pie (totals_amount , labels= None  , startangle= 215 , autopct='%1.1f%%' ,pctdistance= 1.3 , radius= 0.9)
    ax.set_title( trans_type.capitalize()+ " by Category")
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
    print("income vs expenses chart dates from " + iso_date_from + "to " + iso_date_to)

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

def daily_spend (frame,user_id,date_from, date_to):
    for widget in frame.winfo_children():
        widget.destroy()

    iso_date_from = datetime.datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
    iso_date_to = datetime.datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
    list_of_transactions = be.Transaction.getAllTransactionsByMemberIdGroupedByDay(user_id,"EXPENSE", iso_date_from,iso_date_to)
    print("daily spend data:", list_of_transactions)

    days = []
    amount_spend =[]
    for column in list_of_transactions:
        days.append(datetime.datetime.strptime(column [1], "%Y-%m-%d").strftime("%d-%m-%Y"))
        amount_spend.append (column [0])


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
