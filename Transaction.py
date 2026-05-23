import datetime
from dbtools import conn,cursor,sqlite3
from Category import Category
from Member import Member

currentDateTime = datetime.datetime.now()

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
        
    def getAllTransactionsByMemberId(memberId):
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return None
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute('SELECT "transaction".transaction_name, "transaction".transaction_type, "transaction".amount, "transaction".transaction_date, category.category_name FROM "transaction" JOIN category ON "transaction".category_id = category.category_id WHERE category.member_id=:member_id', {'member_id': memberId})
                transactions = cursor.fetchall()
                print(f"Here are the transactions of the {user}. \n {transactions}")
                return transactions
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return []
                # return False

    def getAllAmountByMemberIdFilterByTransactionType(memberId,transactionType):                    #method to get the total amount of income or expenses of a user 
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return None
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute('SELECT SUM("transaction".amount) AS total_amount FROM "transaction" JOIN category ON "transaction".category_id = category.category_id WHERE category.member_id=:member_id AND "transaction".transaction_type =:transaction_type',
                                    {'member_id': memberId, 'transaction_type': transactionType})
                total = cursor.fetchone()
                return total[0]
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return 0
                # return False

        
    def getAllTransactionsByMemberIdFilterDate(memberId,fromDate, tillDate):
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return None
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute('SELECT "transaction".transaction_name, "transaction".transaction_type, "transaction".amount, "transaction".transaction_date, category.category_name FROM "transaction" JOIN category ON "transaction".category_id = category.category_id WHERE category.member_id=:member_id AND "transaction".transaction_date BETWEEN :fromDate AND :tillDate',
                                    {'member_id': memberId, 'fromDate':fromDate, 'tillDate': tillDate})
                transactions = cursor.fetchall()
                print(f"Here are the transactions of the {user}. \n {transactions}")
                return transactions
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return []
                # return False

    def getAllTransactionsByCategoryId(categoryId):                 # method to get all transactions of a member from the db
        tempCategory = Category.getCategoryByCategoryId(categoryId)
        if tempCategory == None:
            return None
        else:    
            try:
                with conn:
                    cursor.execute('SELECT * FROM "transaction" WHERE category_id=:category_id', {'category_id': categoryId})
                transactions = cursor.fetchall()
                print(f"Here are the transactions of the {tempCategory.categoryName}. \n {transactions}")
                return transactions
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return []
                return False
        
    def UpdateTransactionByTransactionId(transactionId,updatedTransaction):             # method to edit a transaction of a member from the db
        tempTransaction = Transaction.getTransactionByTransactionId(transactionId)
        if tempTransaction == None:                                  # no category found to be deleted
            return False
        else:
            try:
                with conn:
                    cursor.execute('UPDATE "transaction" SET transaction_name=:transaction_name, transaction_type, amount, transaction_date, category_id  WHERE transaction_id=:transactionId',
                    {'transaction_name':updatedTransaction.transactionName, 'transaction_type':updatedTransaction.transactionType,  'amount':updatedTransaction.amount, 'transaction_date':updatedTransaction.date, 'category_id':updatedTransaction.categoryId, 'transactionId':transactionId})
                print(f"Updated transaction name to:{tempTransaction.transactionName}.")
                return True                                
            except sqlite3.IntegrityError:
                print("Transaction:This action is restricted, check if all the fields are valid and try again.")
                return False

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
    
    def getAllTransactionsByMemberIdFilterByType(memberId,transactionType):     #This method can be used to get all the expenses or income of a user
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return None
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute('SELECT "transaction".transaction_name, "transaction".amount, "transaction".transaction_date, category.category_name FROM "transaction" JOIN category ON "transaction".category_id = category.category_id WHERE category.member_id=:member_id AND "transaction".transaction_type =:transaction_type', {'member_id': memberId,'transaction_type':transactionType})
                transactions = cursor.fetchall()
                print(f"Here are the {transactionType} transactions of the {user}. \n {transactions}")
                return transactions
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return []
                return False

    def getAllTransactionsByMemberIdGroupedByCategory(memberId):
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return None
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute('SELECT category.category_name, "transaction".amount FROM "transaction" JOIN category ON "transaction".category_id = category.category_id WHERE category.member_id=:member_id', {'member_id': memberId})
                transactions = cursor.fetchall()
                print(f"Here are the transactions of each category of the {user}. \n {transactions}")
                return transactions
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return []
                # return False
