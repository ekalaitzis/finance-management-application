


class Family:
    def __init__(self,familyId, familyName):
        self.familyId = familyId
        self.familyName = familyName

    def __str__(self):
        return f"This is the {self.familyName} Family!"

        

    
class Member:
    def __init__(self, memberId,familyId, firstName, lastName, email, password):
        self.id = memberId
        self.family_id = familyId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def __str__(self):
        m1 = "First name:" + str(self.firstName) + "\n"
        m2 = "Last name:" + str(self.lastName) + "\n"
        m3 = "Email:" + str(self.email)

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