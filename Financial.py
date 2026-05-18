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

    def createMember(self):            # method to add user to the db
        try:
            with conn:
                cursor.execute("INSERT INTO member (first_name, last_name, username, password) VALUES (?,?,?,?)",
                (self.firstName, self.lastName, self.username, self.password))
            self.memberId = cursor.lastrowid
            Category.addDefaultCategories(self)         # on creation of a user add the default categries
            conn.commit()
            passw = "*" * len(self.password)
            print(f"Added member to the DB. Welcome {self.firstName}, {self.lastName} with username {self.username} and password {passw}.")
            return True         # If the addition was succesfull display a message like the above
        except sqlite3.IntegrityError:
            print("This action is restricted, check if all the fields are valid and try again.")
            return False         # If the addition was not succesfull display an error message, this is if the user already exists or a null value is given

    def getMemberByMemberId(memberId):
        cursor.execute("SELECT * FROM member WHERE member_id=:member_id", {'member_id': memberId})
        row = cursor.fetchone()
        member = Member(row[1], row[2], row[3], row[4], row[0])
        return member
    
    def getMemberUsername(self):
        return self.username
    
    def getAllMembers():
        pass

    def updateMemberByid():
        pass

    def deleteMemberByid():
        pass


class Category:
    def __init__(self, categoryName, memberId, categoryId= None):
        self.categoryId = categoryId
        self.categoryName = categoryName
        self.memberId = memberId

    def __str__(self):
        c1 = "Category:" + str(self.categoryName) + "\n"
        c2 = "Member Id:" + str(self.memberId)
        return c1 + c2

    def addDefaultCategories(self):          # method to add to the default categries to the db
        try:
            with conn:
                for category in DEFAULT_CATEGORIES:
                    cursor.execute("INSERT INTO category (category_name,member_id) VALUES (?,?)",
                (category, self.memberId))
            user = Member.getMemberUsername(self)
            print(f"Added the default categories to {user}.")
            return True
        except sqlite3.IntegrityError:
            print("This action is restricted, check if all the fields are valid and try again.")
            return False

    def createCategory(self, member):               #method to add new category to a user
        user = member.username
        print(str(member.memberId) + " = member id " + str(user) + " = username")
        try:
            with conn:
                cursor.execute("INSERT INTO category (category_name,member_id) VALUES (?,?)",
            (self.categoryName, member.memberId))
            print(f"Added the {self.categoryName} category to {user}.")
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("This action is restricted, check if all the fields are valid and try again.")
            return False
        
    def getCategoriesByMemberId(memberId):
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

    def getAllCategoriesByMemberId():
        pass
    def UpdateCategoryByCategoryId():
        pass
    def getAllCategoriesByMemberId():
        pass
    def deleteCategoryByCategoryId():
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

    def createTransaction():
        pass
    def getAllTransactionsByMemberId():
        pass
    def UpdateTransactionByTransactionId():
        pass
    def deleteTransactionByTransactionId():
        pass
        
def menu(self):
        while True:
            print("\n=== Διαχείριση Φοιτητών ===")
            print("1. Add a new Member")
            print("2. Show Members")
            print("3. Update Member")
            print("4. Delete Member")

            print("5. Add Category to Member")
            print("6. Show all Categories of a Member")
            print("7. Update a category of a Member")
            print("8. Delete a category of a Member")

            print("0. Έξοδος")
            choice = input("Επιλέξτε μια ενέργεια: ")

            if choice == '1':
                Member.createMember()
            elif choice == '2':
                Member.getAllMembers()
            elif choice == '3':
                Member.updateMemberByid()
            elif choice == '4':
                Member.deleteMemberByid()

            elif choice == '5':     
                Category.createCategory()
            elif choice == '6':     
                Category.getAllCategoriesByMemberId()
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

    m1 = Member("George", "Tsoukalas", "Gtsouk3", "secret")
    m1.createMember()
    c1 = Category("Temporary", m1.memberId)
    c1.createCategory(m1)
    print("Hello")
    Category.getCategoriesByMemberId(m1.memberId)

if __name__ == "__main__":
    main()