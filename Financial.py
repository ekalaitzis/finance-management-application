


class Family:
    def __init__(self,familyId, familyName):
        self.familyId = familyId
        self.familyName = familyName

    def __str(self):
        return f"This is the {self.familyName} Family!"

        

    def createFamily():
        pass
    def updateFamily():
        pass
    def printFamily():
        pass
    def deleteFamily():
        pass
    
class Member:
    def __init__(self, memberId,familyId, firstName, lastName, email, password):
        self.id = memberId
        self.family_id = familyId
        self.first_name = firstName
        self.last_name = lastName
        self.email = email
        self.password = password

    def __str(self):
        m1 = "First name:" + str(self.firstName) + "\n"
        m2 = "Last name:" + str(self.lastName) + "\n"
        m3 = "Email:" + str(self.email)

        return m1 + m2 + m3
    
    def createMember():
        pass
    def updateMember():
        pass
    def printMember():
        pass
    def deleteMember():
        pass

class Category:
    def __init__(self,categoryId, categoryName, memberId):
        self.id = categoryId
        self.categoryName = categoryName
        self.memberId = memberId


    def __str(self):
        c1 = "Category:" + str(self.categoryName) + "\n"
        c2 = "Member Id:" + str(self.memberId)
        return c1 + c2
    
    def createCategory():
        pass
    def updateCategory():
        pass
    def printCategory():
        pass
    def deleteCategory():
        pass

class Transaction:
    def __init__(self, transactionName, transactionType, amount, date, categoryId):
        self.transactionName = transactionName
        self.transactionType = transactionType
        self.amount = amount
        self.date = date
        self.categoryId = categoryId


    def __str(self):
        t1 = "Transaction name:" + str(self.transactionName) + "\n"
        t2 = "Transaction type:" + str(self.transactionType) + "\n"
        t3 = "Amount:" + str(self.amount) + "\n"
        t4 = "Date:" + str(self.date) + "\n"
        t5 = "Category Id:" + str(self.categoryId)
        return t1 + t2 + t3 + t4 + t5    
    
    def createTransaction():
        pass
    def updateTransaction():
        pass
    def printTransaction():
        pass
    def deleteTransaction():
        pass








def main():
    print("Hello")