import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#fake data
categories = [
    (1, "Groceries", 1),
    (2, "Shopping", 1),
    (3, "Restaurants", 1),
    (4, "Transportation", 1),
    (5, "Travel", 1),
    (6, "Entertainment", 1),
    (7, "Health", 1),
    (8, "General", 1),
    (9, "Utilities", 1),
    (10, "ATM deposit/withdrawal", 1),
    (11, "Investing", 1),
    (12, "Loan", 1),
    (13, "Rent", 1),
    (14, "Donations", 1),
    (15, "Salary", 1),
    (16, "Gift", 1)
]

transactions = [
    (1, "Lidl groceries", "expense", 54.20, "2026-05-01", 1),
    (2, "Zara shirt", "expense", 29.99, "2026-05-02", 2),
    (3, "Dinner at Time Out Market", "expense", 18.50, "2026-05-02", 3),
    (4, "Metro card recharge", "expense", 40.00, "2026-05-03", 4),
    (5, "Flight to Barcelona", "expense", 120.00, "2026-05-04", 5),
    (6, "Netflix subscription", "expense", 12.99, "2026-05-05", 6),
    (7, "Pharmacy medicine", "expense", 9.75, "2026-05-05", 7),
    (8, "Random purchase", "expense", 15.00, "2026-05-06", 8),
    (9, "Electricity bill", "expense", 65.30, "2026-05-07", 9),
    (10, "ATM withdrawal", "expense", 50.00, "2026-05-08", 10),
    (11, "ETF investment", "expense", 200.00, "2026-05-09", 11),
    (12, "Loan payment", "expense", 150.00, "2026-05-10", 12),
    (13, "Monthly rent", "expense", 850.00, "2026-05-01", 13),
    (14, "Charity donation", "expense", 20.00, "2026-05-11", 14),
    (15, "Monthly salary", "income", 2500.00, "2026-05-01", 15),
    (16, "Birthday gift received", "income", 100.00, "2026-05-12", 16),
    (17, "Uber ride", "expense", 13.40, "2026-05-13", 4),
    (18, "Restaurant brunch", "expense", 22.90, "2026-05-14", 3),
    (19, "Supermarket Continente", "expense", 68.10, "2026-05-15", 1),
    (20, "Spotify subscription", "expense", 10.99, "2026-05-16", 6)
]


# =========================
# Pie chart
# =========================

# =========================
# Bar chart
# =========================

def income_vrs_expenses(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    total_income=0
    total_expenses=0
    for t in transactions:
        if t[2] == "income":
            total_income += t[3]
        else:
            total_expenses+=t[3]

    money_type= ["Income","Expenses"]
    total_value = [round(total_income,2 ), round(total_expenses,2)]

    fig,ax=plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.2, right=0.9)


    bars= ax.barh(money_type,total_value, color= ["green", "red"])

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