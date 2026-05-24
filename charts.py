import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import bbox_artist
from unicodedata import category

import Financial as be



# =========================
# Pie chart
# =========================

def expenses_pie_chart (frame,user_id):
    for widget in frame.winfo_children():
        widget.destroy()

    all_expenses_transactions = be.Transaction.getAllTransactionsByMemberIdFilterByType(user_id,"EXPENSE")
    total_amount_per_category={}
    for name,amount,date,categories in all_expenses_transactions:
        if categories in total_amount_per_category:
            total_amount_per_category[categories] += amount
        else:
            total_amount_per_category[categories]=amount
    total_amount_per_category = dict(sorted(total_amount_per_category.items(), key=lambda x: x[1], reverse=True))
    totals_amount = list(total_amount_per_category.values())
    unique_categories = list (total_amount_per_category.keys())

    fig, ax = plt.subplots(figsize=(5, 3),constrained_layout=True)
    ax.pie (totals_amount , labels= None  , startangle= 215 , autopct='%1.1f%%' ,pctdistance= 1.2 , radius= 0.9)
    ax.set_title("Expenses by Category")
    ax.legend (unique_categories, loc = "lower left" , bbox_to_anchor=(1,0))

    canvas = FigureCanvasTkAgg(fig, master= frame )
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(columnspan=2 )


# =========================
# Bar chart
# =========================

def income_vrs_expenses(frame,user_id):
    for widget in frame.winfo_children():
        widget.destroy()

    total_income= be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_id,"INCOME")
    total_expenses=be.Transaction.getAllAmountByMemberIdFilterByTransactionType(user_id,"EXPENSE")


    money_type= ["Expenses","Income"]
    total_value = [round(total_expenses,2), round(total_income,2 )]

    fig,ax=plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.2, right=0.9)


    bars= ax.barh(money_type,total_value, color= ["red" , "green"])

    for i, bar in enumerate(bars):
        width = bar.get_width()

        ax.text( width / 2, bar.get_y() + bar.get_height() / 2, str(total_value[i]), ha='center', va='center', color='white', fontweight='bold' )
    ax.set_title ("Income vs Expenses")


    canvas = FigureCanvasTkAgg(fig, master= frame )
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(columnspan=2 )

# =========================
# Line chart
# =========================