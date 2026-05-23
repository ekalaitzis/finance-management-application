from dbtools import conn,cursor,sqlite3
from Transaction import Transaction
from Category import Category


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
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:
            return None
        else:
            try:
                with conn:
                    cursor.execute("UPDATE member SET first_name=:firstName, last_name=:lastName, password=:password WHERE member_id=:memberId",
                    {'firstName':updatedMember.firstName, 'lastName':updatedMember.lastName, 'password':updatedMember.password, "memberId":tempMember.memberId})
                passw = "*" * len(updatedMember.password)
                print(f"Updated member:{tempMember.username} {tempMember.firstName}, {tempMember.lastName} with password {passw}.")
                return True                                
            except sqlite3.IntegrityError:
                print("Member:This action is restricted, check if all the fields are valid and try again.")
                return False

    def deleteMemberByMemberId(memberId):                             # method to delete a member from the db
        tempMember = Member.getMemberByMemberId(memberId)
        if tempMember == None:                                  # no member found to be deleted
            return None
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
