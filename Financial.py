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
        self.memberId = memberId
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password

    def __str__(self):
        m1 = "First name:" + str(self.firstName) + "\n"
        m2 = "Last name:" + str(self.lastName) + "\n"
        m3 = "Username:" + str(self.username)

        return m1 + m2 + m3

    def createMember(self):                             # method to add user to the db
        try:
            with conn:
                cursor.execute("INSERT INTO member (first_name, last_name, username, password) VALUES (?,?,?,?)",
                (self.firstName, self.lastName, self.username, self.password))
            self.memberId = cursor.lastrowid
            Category.addDefaultCategories(self)         # on creation of a user add the default categries
            conn.commit()
            passw = "*" * len(self.password)
            print(f"Added member to the DB. Welcome {self.firstName}, {self.lastName} with username {self.username} and password {passw}.")
            return True                                 # If the addition was succesfull display a message like the above
        except sqlite3.IntegrityError:
            print("Member:This action is restricted, check if all the fields are valid and try again.")
            return False                                # If the addition was not succesfull display an error message, this is if the user already exists or a null value is given

    def getMemberByMemberId(memberId):                  # method to add user to the db
        cursor.execute("SELECT * FROM member WHERE member_id=:member_id", {'member_id': memberId})
        row = cursor.fetchone()
        member = Member(row[1], row[2], row[3], row[4], row[0])
        return member
    
    def getAllMembers():                                # method to get all members from the db
        cursor.execute("SELECT * FROM member")
        row = cursor.fetchall()
        for member in row:
            print(member)
        return row

    def updateMemberByid():                             # method to edit a member in the db
        pass

    def deleteMemberByid():                             # method to delete a member from the db
        pass    

    def getMemberUsername(self):                        ## temp, to be deleted
        return self.username
    
class Category:
    def __init__(self, categoryName, memberId, categoryId= None):
        self.categoryId = categoryId
        self.categoryName = categoryName
        self.memberId = memberId

    def __str__(self):
        c1 = "Category:" + str(self.categoryName) + "\n"
        c2 = "Member Id:" + str(self.memberId)
        return c1 + c2

    def addDefaultCategories(self):                     # method to add to the default categries to the db
        user = Member.getMemberUsername(self)
        try:
            with conn:
                for category in DEFAULT_CATEGORIES:
                    cursor.execute("INSERT INTO category (category_name,member_id) VALUES (?,?)",
                (category, self.memberId))
            print(f"Added the default categories to {user}.")
            return True
        except sqlite3.IntegrityError:
            print("Category:This action is restricted, check if all the fields are valid and try again.")
            return False

    def createCategoryByMemberId(self, memberId):                   #method to add new category to a member
        member = Member.getMemberByMemberId(memberId)
        user = member.username
        try:
            with conn:
                cursor.execute("INSERT INTO category (category_name,member_id) VALUES (?,?)",
            (self.categoryName, memberId))
            print(f"Added the {self.categoryName} category to {user}.")
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("This action is restricted, check if all the fields are valid and try again.")
            return False
        
    def getAllCategoriesByMemberId(memberId):           # method to get all categories of a member from the db
        member = Member.getMemberByMemberId(memberId)
        user = member.username
        try:
            with conn:
                cursor.execute("SELECT * FROM category WHERE member_id=:member_id", {'member_id': memberId})
            categories = cursor.fetchall()
            print(f"Here are the categories of the {user}. \n {categories}")
            return True
        except sqlite3.IntegrityError:
            print("This action is restricted, check if all the fields are valid and try again.")
            return False

    def UpdateCategoryByCategoryId():                   # method to edit a category of a member from the db
        pass

    def deleteCategoryByCategoryId():                   # method to delete a category of a member from the db
        pass
        
class Transaction:
    def __init__(self, transactionName, transactionType, amount, date, categoryId, transactionId=None):
        self.transactionId = transactionId
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

    def createTransaction():                            #method to add new transaction to a member
        pass
    def getAllTransactionsByMemberId():                 # method to get all transactions of a member from the db
        pass
    def UpdateTransactionByTransactionId():             # method to edit a transaction of a member from the db
        pass
    def deleteTransactionByTransactionId():             # method to delete a transaction of a member from the db
        pass
        
def menu():
        while True:
            print("\n=== Διαχείριση Φοιτητών ===")
            print("1. Add a new Member")
            print("2. Show all Members")
            print("3. Update Member")
            print("4. Delete Member")
            print("5. Add Category to Member")
            print("6. Show all Categories of a Member")
            print("7. Update a Category of a Member")
            print("8. Delete a Category of a Member")
            print("11. Add Transaction to Member")
            print("12. Show all Transactions of a Member")
            print("13. Update a Transaction of a Member")
            print("14. Delete a Transaction of a Member")

            print("0. Έξοδος")
            choice = input("Επιλέξτε μια ενέργεια: ")

            if choice == '1':
                name = input("First name? ")
                lastName = input("Last name? ")
                username = input("username? ")
                password = input("Password? ")
                
                m1 = Member(name, lastName, username, password)
                m1.createMember()
            elif choice == '2':
                Member.getAllMembers()
            elif choice == '3':
                Member.updateMemberByid()
            elif choice == '4':
                Member.deleteMemberByid()

            elif choice == '5':
                cat = input("Insert category name: ")
                id = int(input("Insert member id: "))
                c1 = Category(cat, id)
                c1.createCategoryByMemberId(id)
            elif choice == '6':
                id = int(input("Select member id:"))
                Category.getAllCategoriesByMemberId(id)
            elif choice == '7':
               Category.UpdateCategoryByCategoryId()
            elif choice == '8':
                Category.deleteCategoryByCategoryId()

            elif choice == '11':
                Transaction.createTransaction()
            elif choice == '12':
                Transaction.getAllTransactionsByMemberId()
            elif choice == '13':
               Transaction.UpdateTransactionByTransactionId()
            elif choice == '14':
                Transaction.deleteTransactionByTransactionId()
            
            elif choice == '0':
                print("Bye!")
                break

def main():
    menu()

    # m1 = Member("George", "Tsoukalas", "Gtsouk3", "secret")
    # m1.createMember()
    # c1 = Category("Temporary", m1.memberId)
    # c1.createCategory(m1)
    # print("Hello")
    # Category.getCategoriesByMemberId(m1.memberId)

if __name__ == "__main__":
    main()