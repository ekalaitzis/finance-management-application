import xlsxwriter
from Financial import Transaction


# Export συναλλαγών σε excel

def export_to_excel(member_id, from_date=None, to_date=None,
                    filename=None):
    if filename is None:
        filename = "oikonomika_stoixeia.xlsx"

    transactions = Transaction.getAllTransactionsByMemberId(
        member_id,
        from_date,
to_date)

    workbook = xlsxwriter.Workbook(filename)

    worksheet = workbook.add_worksheet("Συναλλαγές")

    headers = [
        "Περιγραφή",
        "Τύπος",
        "Ποσό",
        "Ημερομηνία",
        "Κατηγορία"
    ]

    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    for row_num, transaction in enumerate(transactions, start=1):

        transaction_name = transaction[1]
        transaction_type = transaction[2]
        amount = transaction[3]
        date = transaction[4]
        category_name = transaction[7]

        worksheet.write(row_num, 0, transaction_name)
        worksheet.write(row_num, 1, transaction_type)
        worksheet.write(row_num, 2, amount)
        worksheet.write(row_num, 3, date)
        worksheet.write(row_num, 4, category_name)

    workbook.close()

    print("Το αρχείο excel δημιουργήθηκε.")

    return filename


# Παράδειγμα χρήσης:
# export_to_excel(1, "2026-05-01", "2026-05-31")
