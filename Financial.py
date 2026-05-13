


class Family:
    def __init__(self,familyId, familyName):
        self.familyId = familyId
        self.familyName = familyName

    def __str(self):
        return f"this is the {self.familyName} Family!"

        

    def createFamily():
        pass
    def updateFamily():
        pass
    def printFamily():
        pass
    def deleteFamily():
        pass
    
class Member:
    def __init__(self, id,familyId, firstName, lastName, email, password):
        self.id = id
        self.family_id = familyId
        self.first_name = firstName
        self.last_name = lastName
        self.email = email
        self.password = password

    def __str(self):
        m1 = "First name:" + str(self.firstName) + "\n"
        m2 = "Last name:" + str(self.lastName) + "\n"
        m3 = "Email:" + str(self.email) + "\n"

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
    def __init__(self,id, categoryName, memberId):
        self.id = id
        self.categoryName = categoryName
        self.memberId = memberId


    def __str(self):

        pass

    
    def createCategory():
        pass
    def updateCategory():
        pass
    def printCategory():
        pass
    def deleteCategory():
        pass

class Transaction:
    def __init__(self):
        

     pass

    def __str(self):

        pass
    
    
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