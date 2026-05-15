import sqlite3

DEFAULT_CATEGORIES = [
    "Groceries", "Shopping", "Restaurants", "Transportation",
    "Travel", "Entertainment", "Health", "General",
    "Utilities", "ATM deposit/withdrawal", "Investing",
    "Loan", "Rent", "Donations", "Salary", "Gift"
]


conn = sqlite3.connect('Finance.db')
cursor = conn.cursor()


class Family:
    def __init__(self,familyId, familyName):
        self.familyId = familyId
        self.familyName = familyName

    def __str__(self):
        return f"This is the {self.familyName} Family!"
        
    def createFamily(self, fname):
        cursor.execute("INSERT INTO family (family_name) VALUES (?)", (fname,))
        self.familyId = cursor.lastrowid
        self.familyName = fname
        conn.commit() 
        
        
    def deleteFamily(self, fname):
        cursor.execute("DELET FROM family WHERE family_name = ?", (fname,))
        self.familyId = None
        self.familyName = None
        conn.commit() 

    
class Member:
    def __init__(self, memberId,familyId, firstName, lastName,username, password):
        self.id = memberId
        self.family_id = familyId
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password

    def __str__(self):
        m1 = "First name:" + str(self.firstName) + "\n"
        m2 = "Last name:" + str(self.lastName) + "\n"
        m3 = "Username:" + str(self.username)

        return m1 + m2 + m3
    

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
    print("Hello")