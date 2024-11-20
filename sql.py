import sqlite3
import hashlib

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

#---------------------------------------------------------------------------
def hash_info(password):
    # default utf-8
    pwd_byte = password.encode()
    pwd_hash = hashlib.sha256()

    pwd_hash.update(pwd_byte)

    # get hex-string
    pwd_hash = str(pwd_hash.hexdigest())

    return pwd_hash

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except sqlite3.Error as error:
                print(string)
                print(error)
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()
        self.execute("DROP TABLE IF EXISTS Messages")
        self.commit()
        self.execute("DROP TABLE IF EXISTS Friends")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0,
            pk TEXT,
            salt TEXT
        )""")

        self.commit()

        # Create the messages table
        self.execute("""CREATE TABLE Messages(
            Id INTEGER PRIMARY KEY,
            sender TEXT REFERENCES Users(username),
            receiver TEXT REFERENCES Users(username),
            message TEXT
        )""")

        self.commit()

        # Create the friends table
        self.execute("""CREATE TABLE Friends(
            user TEXT REFERENCES Users(username),
            friend TEXT REFERENCES Users(username)
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, 'no', '4', admin=1)

        # # Add 2 sample users
        pwd = self.hash_info('1234')
        self.add_user('may', pwd, 'no', '4', admin=0)
        self.add_user('dzaka', pwd, 'no', '4', admin=0)

        # # Adding each other as friend
        self.add_friend('may', 'dzaka')
        self.add_friend('dzaka', 'may')

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, pk, salt, admin=0):

        sql_cmd = """
                INSERT INTO Users
                (username, password, pk, salt, admin)
                VALUES('{username}', '{password}', '{pk}', '{salt}', {admin})
            """

        sql_cmd = sql_cmd.format(username=username, \
            password=password, pk=pk, salt=salt, admin=admin)

        self.execute(sql_cmd)
        self.commit()

        success = self.check_credentials(username, password)
        if success == True:
            return True
        else:
            return False

    #-----------------------------------------------------------------------------

    # Add a message
    def add_message(self, sender, receiver, message):
        sql_cmd = """
                INSERT INTO Messages
                (sender, receiver, message)
                VALUES('{sender}', '{receiver}', '{message}')
            """
        
        sql_cmd = sql_cmd.format(sender=sender, \
            receiver=receiver, message=message)

        self.execute(sql_cmd)
        self.commit()

        return True

    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_friend(self, user, friend):
        sql_cmd = """
                INSERT INTO Friends
                (user, friend)
                VALUES('{user}', '{friend}')
            """

        sql_cmd = sql_cmd.format(user=user, friend=friend)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):

        sql_query = """
                SELECT *
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, \
            password=password)
        
        self.execute(sql_query)
        result = self.cur.fetchone()
        #print(result)
        # If our query returns
        if result != None:
            return True
        else:
            return False
    
    #-----------------------------------------------------------------------------

    # get user
    def get_user(self, username):
        sql_query = """
                SELECT *
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        
        self.execute(sql_query)
        result = self.cur.fetchone()
        # print(pwd_hash, result)

        # If our query returns
        if result != None:
            return result[1]
        else:
            return None

    #-----------------------------------------------------------------------------
    # get message
    def get_message(self, sender, receiver):
        sql_query = """
                SELECT *
                FROM Messages
                WHERE sender = '{sender}' AND receiver = '{receiver}'
                ORDER BY Id
            """
        
        sql_query = sql_query.format(sender=sender, \
            receiver=receiver)
        
        self.execute(sql_query)
        result = self.cur.fetchall()

        # If our query returns
        #print(result)
        if result:
            # This is to handle if there's more than one message
            for i in range(len(result)):
                result[i] = result[i][3]
            #print(result)
            return result
        else:
            return None

    #-----------------------------------------------------------------------------

    # Get friends
    def get_friends(self, user):
        sql_query = """
                SELECT *
                FROM Friends
                WHERE user = '{user}'
            """

        sql_query = sql_query.format(user=user)
        
        self.execute(sql_query)
        
        # If our query returns
        result = self.cur.fetchone()
        
        if result != None:
            return result[1]
        else:
            return None

    #-----------------------------------------------------------------------------

    # Check if friends
    def is_friend(self, user, name):
        sql_query = """
                SELECT *
                FROM Friends
                WHERE user = '{user}'
            """

        sql_query = sql_query.format(user=user)
        
        self.execute(sql_query)
        
        # If our query returns
        result = self.cur.fetchall()
        #print(result)
        if result == None:
            return False

        for row in result:
            if row[1] == name:
                return True
        
        return False

    #-----------------------------------------------------------------------------

    # Get a user and its password
    def get_user_and_pwd(self, username):
        sql_query = """
                SELECT *
                FROM Users
                WHERE username = '{username}'
            """
        
        sql_query = sql_query.format(username=username)

        result = self.execute(sql_query)
        
        # If our query returns
        result = result.fetchone()
        
        if result != None:
            return result[1], result[2], result[5]
        else:
            return None

    #-----------------------------------------------------------------------------

    def get_friend_pks(self, user):
        sql_query = """
                SELECT *
                FROM Friends F JOIN Users U ON(F.friend = U.username)
                WHERE user = '{user}'
            """
        
        sql_query = sql_query.format(user=user)

        self.execute(sql_query)
        result = self.cur.fetchall()

        dt = {}
        for i in range(len(result)):
            dt[result[i][1]] = result[i][6]
            
        return dt

     #-----------------------------------------------------------------------------

    def get_salt(self, user):
        sql_query = """
            SELECT salt
            FROM Users
            WHERE username = '{user}'
        """

        sql_query = sql_query.format(user=user)

        self.execute(sql_query)
        result = self.cur.fetchone()
        #print(result)
        if result != None:
            return result[0]
        else:
            return None

    #-----------------------------------------------------------------------------
    
    def delete_user(self, username):
        sql_query = """
                DELETE FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        self.commit()

    #-----------------------------------------------------------------------------
    
    def delete_friend(self, user, friend):
        sql_query = """
                DELETE FROM Friends
                WHERE user = '{user}' AND friend = '{friend}'
            """

        sql_query = sql_query.format(user=user, friend=friend)

        self.execute(sql_query)
        self.commit()

    #-----------------------------------------------------------------------------

    def hash_info(self, password):
        # default utf-8
        pwd_byte = password.encode()
        pwd_hash = hashlib.sha256()

        pwd_hash.update(pwd_byte)

        # get hex-string
        pwd_hash = str(pwd_hash.hexdigest())

        return pwd_hash
