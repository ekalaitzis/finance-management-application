import xlsxwriter
import sqlite3

# Εξαγωγή συναλλαγών σε Excel

def export_to_excel(filename="oikonomika_stoixeia.xlsx"):

    conn = sqlite3.connect('Finance.db')
    cursor = conn.cursor()

    sql_query = """
    SELECT transaction_name, transaction_type, amount, date
    FROM "transaction"
    """

    cursor.execute(sql_query)

    transactions = cursor.fetchall()

    workbook = xlsxwriter.Workbook(filename)

    worksheet = workbook.add_worksheet("Συναλλαγές")

    headers = ["Περιγραφή", "Τύπος", "Ποσό", "Ημερομηνία"]

    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    for row_num, row_data in enumerate(transactions, start=1):
        for col_num, data in enumerate(row_data):
            worksheet.write(row_num, col_num, data)

    workbook.close()

    conn.close()

    print("Η εξαγωγή ολοκληρώθηκε!")

export_to_excel()