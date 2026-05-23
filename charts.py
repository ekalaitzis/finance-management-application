import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Financial as be



# =========================
# Pie chart
# =========================

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