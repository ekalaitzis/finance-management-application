from dbtools import conn,cursor,sqlite3
from Transaction import Transaction
from Member import Member


DEFAULT_CATEGORIES = [
    "Groceries", "Shopping", "Restaurants", "Transportation",
    "Travel", "Entertainment", "Health", "General",
    "Utilities", "ATM deposit/withdrawal", "Investing",
    "Loan", "Rent", "Donations", "Salary", "Gift"
]




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
            return None
        else:
            user = tempMember.username
            try:
                with conn:
                    cursor.execute("SELECT * FROM category WHERE member_id=:member_id", {'member_id': memberId})
                categories = cursor.fetchall()
                print(f"Here are the categories of the {user}. \n {categories}")
                return categories
                # return True
            except sqlite3.IntegrityError:
                print("This action is restricted, check if all the fields are valid and try again.")
                return []
                # return False
 
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
        