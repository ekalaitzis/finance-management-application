import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Financial as be

# =========================
# total income and total expenses
# =========================
def total_income_by_user (user_id):
    total_income=0
    for t in be.Transaction.getAllTransactionsByMemberId(user_id):
        if t[1] == "INCOME":
            total_income += t[2]
    return total_income

def total_expences_by_user (user_id):
    total_expenses=0
    for t in be.Transaction.getAllTransactionsByMemberId(user_id):
        if t[1] == "EXPENSE":
            total_expenses += t[2]
    return total_expenses

# =========================
# Pie chart
# =========================

# =========================
# Bar chart
# =========================

def income_vrs_expenses(frame,user_id):
    for widget in frame.winfo_children():
        widget.destroy()

    total_income=0
    total_expenses=0
    for t in be.Transaction.getAllTransactionsByMemberId(user_id):
        if t[1] == "INCOME":
            total_income += t[2]
        else:
            total_expenses+=t[2]

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