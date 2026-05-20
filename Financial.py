import sqlite3
import datetime

currentDateTime = datetime.datetime.now()

DEFAULT_CATEGORIES = [
    "Groceries", "Shopping", "Restaurants", "Transportation",
    "Travel", "Entertainment", "Health", "General",
    "Utilities", "ATM deposit/withdrawal", "Investing",
    "Loan", "Rent", "Donations", "Salary", "Gift"
]


conn = sqlite3.connect('Finance.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
            passw = "*" * len(self.password)
            print(f"Added member to the DB. Welcome {self.firstName}, {self.lastName} with username {self.username} and password {passw}.")
            return True                                 # If the addition was succesfull display a message like the above
        except sqlite3.IntegrityError:
            print("Member:This action is restricted, check if all the fields are valid and try again.")
            return False                                # If the addition was not succesfull display an error message, this is if the user already exists or a null value is given

    def getMemberByMemberId(memberId):                  # method to add user to the db
        with conn:
            cursor.execute("SELECT * FROM member WHERE member_id=:member_id", {'member_id': memberId})
        row = cursor.fetchone()
        if row == None:
            print(f"No member found with id: {memberId}.")
            return None
        return Member(row[1], row[2], row[3], row[4], row[0])
    
    def getAllMembers():                                # method to get all members from the db
        cursor.execute("SELECT * FROM member")
        row = cursor.fetchall()
        for member in row:
            print(member)
        return row

    def updateMemberByMemberId(memberId,updatedMember):                             # method to edit a member in the db
        currMember = Member.getMemberByMemberId(memberId)
        try:
            with conn:
                cursor.execute("UPDATE member SET first_name=:firstName, last_name=:lastName, password=:password WHERE member_id=:memberId",
                {'firstName':updatedMember.firstName, 'lastName':updatedMember.lastName, 'password':updatedMember.password, "memberId":currMember.memberId})
            passw = "*" * len(updatedMember.password)
            print(f"Updated member:{currMember.username} {currMember.firstName}, {currMember.lastName} with password {passw}.")
            return True                                
        except sqlite3.IntegrityError:
            print("Member:This action is restricted, check if all the fields are valid and try again.")
            return False

    def deleteMemberByMemberId(memberId):                             # method to delete a member from the db
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:                                  # no member found to be deleted
            return False
        else:
            with conn:
                cursor.execute("DELETE FROM member WHERE member_id=:member_id", {'member_id': memberId})
            if Member.getMemberByMemberId(memberId) == None:    #check if deleted
                print(f"User: {tempMember.username} deleted.")
                return True
            else:
                print("Failed to delete")                       
                return False

    def getMemberUsername(self):                        ## temp, to be deleted
        return self.username
    
    def getMemberByUsername(username):                  # method to get member obj with a username, can be used to check if a username exists in the DB
            with conn:
                cursor.execute("SELECT * FROM member WHERE username=:username", {'username': username})
            memnber = cursor.fetchone()
            if memnber:
                return memnber
            else:
                return None

    def validateMember(username, password):             # method to validate a username and password against the DB records,use for login
        member = Member.getMemberByUsername(username)
        if member == None:
            print(f"{username} was not found in the database.")
            return False
        if member[4] == password:
            return True
        else:
            return False

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
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return False
        else:
            try:
                with conn:
                    cursor.execute("INSERT INTO category (category_name,member_id) VALUES (?,?)",
                (self.categoryName, memberId))
                print(f"Added the {self.categoryName} category to {tempMember.username}.")
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return False
            
    def getAllCategoriesByMemberId(memberId):           # method to get all categories of a member from the db
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return False
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute("SELECT * FROM category WHERE member_id=:member_id", {'member_id': memberId})
                categories = cursor.fetchall()
                print(f"Here are the categories of the {user}. \n {categories}")
                return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return False
 
    def getCategoryByCategoryId(categoryId):
        with conn:
            cursor.execute("SELECT * FROM category WHERE category_id=:categoryId", {"categoryId":categoryId})
        row = cursor.fetchone()
        if row == None:
            print(f"No category found with id: {categoryId}.")
            return None
        else:
            print(Category(row[1], row[2], row[0]))
            return Category(row[1], row[2], row[0])

    def UpdateCategoryByCategoryId(categoryId,updatedCategory):                   # method to edit a category of a member from the db
        currCategory = Category.getCategoryByCategoryId(categoryId)
        try:
            with conn:
                cursor.execute("UPDATE category SET category_name=:categoryName WHERE category_id=:categoryId",
                {'categoryName':updatedCategory.categoryName, "categoryId":currCategory.categoryId})
            print(f"Updated category name to:{currCategory.categoryName}.")
            return True                                
        except sqlite3.IntegrityError:
            print("Category:This action is restricted, check if all the fields are valid and try again.")
            return False

    def deleteCategoryByCategoryId(categoryId):                   # method to delete a category of a member from the db
        tempCategory = Category.getCategoryByCategoryId(categoryId)
        if tempCategory == None:                                  # no category found to be deleted
            return False
        else:
            with conn:
                cursor.execute("DELETE FROM category WHERE category_id=:category_id", {'category_id': categoryId})
            if Category.getCategoryByCategoryId(categoryId) == None:    #check if deleted
                print(f"Category: {tempCategory.categoryName} deleted.")
                return True
            else:
                print("Failed to delete")                       
                return False

        
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

    def createTransactionByCategoryId(self, categoryId):                            #method to add new transaction to a member
        tempCategory = Category.getCategoryByCategoryId(categoryId)
        if tempCategory == None:
            return False
        else:
            try:
                with conn:
                    cursor.execute('INSERT INTO "transaction" (transaction_name, transaction_type, amount, transaction_date, category_id) VALUES (?, ?, ?, ?, ?)',
                                   (self.transactionName, self.transactionType ,self.amount ,self.date ,categoryId))
                    print(f"Transaction added! \n{self.transactionName} \n{self.transactionType}\n{self.amount}\n{self.date}\nto:\n{tempCategory}")
                    conn.commit()
                    return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return False
            except sqlite3.OperationalError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return False

    def getTransactionByTransactionId(transactionId):
        with conn:
            cursor.execute('SELECT * FROM "transaction" WHERE transaction_id=:transactionId', {"transactionId":transactionId})
        row = cursor.fetchone()
        if row == None:
            print(f"No category found with id: {transactionId}.")
            return None
        else:
            print(Transaction(row[1], row[2], row[3], row[4], row[5], row[0]))
            return Transaction(row[1], row[2], row[3], row[4], row[5], row[0])
        
    def getAllTransactionsByCategoryId(categoryId):                 # method to get all transactions of a member from the db
        tempCategory = Category.getCategoryByCategoryId(categoryId)
        if tempCategory == None:
            return False
        else:    
            try:
                with conn:
                    cursor.execute('SELECT * FROM "transaction" WHERE category_id=:category_id', {'category_id': categoryId})
                transactions = cursor.fetchall()
                print(f"Here are the transactions of the {tempCategory.categoryName}. \n {transactions}")
                return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return False
        
    def UpdateTransactionByTransactionId():             # method to edit a transaction of a member from the db
        pass

    def deleteTransactionByTransactionId(transactionId):             # method to delete a transaction of a member from the db
        tempTransaction = Transaction.getTransactionByTransactionId(transactionId)
        if tempTransaction == None:                                  # no category found to be deleted
            return False
        else:
            with conn:
                cursor.execute('DELETE FROM "transaction" WHERE transaction_id=:transactionId', {'transactionId': transactionId})
            if Transaction.getTransactionByTransactionId(transactionId) == None:    #check if deleted
                print(f"Transaction: {tempTransaction.transactionName} deleted.")
                return True
            else:
                print("Failed to delete")                       
                return False
        
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
            print("12. Show all Transactions of a Category")
            print("13. Update a Transaction")
            print("14. Delete a Transaction")

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
                id = int(input("Select member id to update:"))
                name = input("New first name? ")
                lastName = input("New last name? ")
                password = input("New password? ")
                tempMember = Member(name, lastName, "temp", password)
                Member.updateMemberByid(id,tempMember)
            elif choice == '4':
                id = int(input("Select member id:"))
                Member.deleteMemberByid(id)

            elif choice == '5':
                cat = input("Insert category name: ")
                id = int(input("Insert member id: "))
                c1 = Category(cat, id)
                c1.createCategoryByMemberId(id)
            elif choice == '6':
                id = int(input("Select member id:"))
                Category.getAllCategoriesByMemberId(id)
            elif choice == '7':
                id = int(input("Select category id to update:"))
                name = input("New categoryy name? ")
                tempCategory = Category(name, 1)
                Category.UpdateCategoryByCategoryId(id,tempCategory)
            elif choice == '8':
                id = int(input("Select category id to delete:"))
                Category.deleteCategoryByCategoryId(id)

            elif choice == '11':
                name = input("Transaction name? ")
                type = int(input("Transaction type? 1 for income, 0 for expense."))
                if type == 1:
                    transactionType = "INCOME"
                else:
                    transactionType = "EXPENSE"
                amount = int(input("Amount of transaction? "))
                catId = input("Category id of the transaction? ")
                
                t1 = Transaction(name, transactionType, amount, currentDateTime, catId)
                t1.createTransactionByCategoryId(catId)
            elif choice == '12':
                id = int(input("Select category id:"))
                Transaction.getAllTransactionsByCategoryId(id)
            elif choice == '13':
                id = int(input("Select transaction id to update:"))
                Transaction.UpdateTransactionByTransactionId(id)
            elif choice == '14':
                id = int(input("Select transaction id to delete:"))
                Transaction.deleteTransactionByTransactionId(id)
            
            elif choice == '0':
                print("Bye!")
                break

def main():
    menu()

if __name__ == "__main__":
    main()