import sqlite3

DEFAULT_CATEGORIES = [
    "Groceries", "Shopping", "Restaurants", "Transportation",
    "Travel", "Entertainment", "Health", "General",
    "Utilities", "ATM deposit/withdrawal", "Investing",
    "Loan", "Rent", "Donations", "Salary", "Gift"
]


conn = sqlite3.connect('Finance.db')
cursor = conn.cursor()

    
class Member:
    def __init__(self, firstName, lastName, username, password, memberId=None):
        self.id = memberId
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password

    def __str__(self):
        m1 = "First name:" + str(self.firstName) + "\n"
        m2 = "Last name:" + str(self.lastName) + "\n"
        m3 = "Username:" + str(self.username)

        return m1 + m2 + m3

    def addMember(self):
        cursor.execute("INSERT INTO member (first_name, last_name, username, password) VALUES (?,?,?,?)",
            (self.firstName, self.lastName, self.username, self.password))
        self.memberId = cursor.lastrowid
        conn.commit()
   

class Category:
    def __init__(self,categoryId, categoryName, memberId):
        self.id = categoryId
        self.categoryName = categoryName
        self.memberId = memberId


    def __str__(self):
        c1 = "Category:" + str(self.categoryName) + "\n"
        c2 = "Member Id:" + str(self.memberId)
        return c1 + c2
    

class Transaction:
    def __init__(self, transactionName, transactionType, amount, date, categoryId):
        self.transactionName = transactionName
        self.transactionType = transactionType
        self.amount = amount
        self.date = date        # this should set to get current date and time maybe timestamp
        self.categoryId = categoryId


    def __str__(self):
        t1 = "Transaction name:" + str(self.transactionName) + "\n"
        t2 = "Transaction type:" + str(self.transactionType) + "\n"
        t3 = "Amount:" + str(self.amount) + "\n"
        t4 = "Date:" + str(self.date) + "\n"  
        t5 = "Category Id:" + str(self.categoryId)
        return t1 + t2 + t3 + t4 + t5    
    


def main():

    m1 = Member("Dimitris", "Tsoukalas", "osfp", "123pass")
    m1.addMember()
    print("Hello")

if __name__ == "__main__":
    main()