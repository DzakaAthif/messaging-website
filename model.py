'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
from os import POSIX_SPAWN_DUP2
import view
import random
import sql
import json
import hashlib

db = sql.SQLDatabase("test.db")
db.database_setup()  # pwd: admin

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

# basic functions------------------------------------------------------
def single_quote(message):
    # check single-quote in messages
    mess_list = []
    for m in message:
        mess_list.append(m)

    j = 0
    while j < len(mess_list):
        if mess_list[j] == "'":
            mess_list.insert(j+1, "'")
            j = j+1
        j = j+1

    message = ''.join(mess_list)
    return message

def hash_info(password):
    # default utf-8
    pwd_byte = password.encode()
    pwd_hash = hashlib.sha256()

    pwd_hash.update(pwd_byte)

    # get hex-string
    pwd_hash = str(pwd_hash.hexdigest())

    return pwd_hash


def get_user_from_ip(ip):
    with open('logged_in.json', 'r') as openfile:
        # Reading from json file
        logged_in = json.load(openfile)

    if ip not in logged_in:
        return None

    return logged_in[ip]
#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("home")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form(ip, mssg):
    '''
        login_form
        Returns the view for the login_form
    '''
    with open('logged_in.json', 'r') as openfile:
        # Reading from json file
        logged_in = json.load(openfile)
    
    if ip in logged_in:
        err_str = f"You have logged in {logged_in[ip]}! :)"
        return page_view("invalid", reason=err_str)

    return page_view("login", login_mssg=mssg)

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password, ip):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # Check if the username is empty. 
    cond1 = username == None or len(username) == 0
    if cond1:
        return login_form(ip, "username is empty")

    # Check if the password is empty.
    cond2 = password == None or len(password) == 0
    if cond2:
        return login_form(ip, "password is empty")

    # Getting the salt while also check if username exist.
    salt = db.get_salt(username)
    if salt == None:
        return login_form(ip, "username does not exists")

    # By default assume good creds.
    login = True
    password = hash_info(password+salt)
    #print(password)
    # Check if the combination is invalid.
    login = db.check_credentials(username, password)  
    if login ==  False: 
        return login_form(ip, "This combination is invalid")

    # Write the ip and the username to the logged_in file.
    with open('logged_in.json', 'r') as openfile:
        # Reading from json file
        logged_in = json.load(openfile)

    logged_in[ip] = username
    json_object = json.dumps(logged_in, indent=4)

    with open('logged_in.json', 'w') as outfile:
        outfile.write(json_object)
        
    return page_view("login_valid", name=username)


#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]

#-----------------------------------------------------------------------------
# Chat
#-----------------------------------------------------------------------------

# def encrypt_message(ip, mssg):
#     '''
#         send
#         sending messages.
#     '''
#     with open('logged_in.json', 'r') as openfile:
#         # Reading from json file
#         logged_in = json.load(openfile)
    
#     # Check if the client already logged_in.
#     if ip not in logged_in:
#         return page_view("not_logged_in")
    
#     # Get the user's friend.
#     fr = db.get_friends(logged_in[ip])  # we can create a friend list

#     return page_view("chat", send_mssgs=mssg, friend=fr)

def chat(ip, mssg):
    '''
        send
        sending messages.
    '''
    print("chat")
    with open('logged_in.json', 'r') as openfile:
        # Reading from json file
        logged_in = json.load(openfile)
    
    # Check if the client already logged_in.
    if ip not in logged_in:
        return page_view("not_logged_in")
    
    # Get the user's friend.
    fr = db.get_friends(logged_in[ip])  # we can create a friend list

    return page_view("chat", mssgs=mssg, friend=fr)

def create_chat(ip, friend, message):
    # Check if the user doesnt pick any friend.
    if friend == None or len(friend) == 0:
        return chat(ip, "")

    # Check if the message is empty.
    if message == None or len(message) == 0:
        return chat(ip, "")

    # Get the username of the cur client.
    user = get_user_from_ip(ip)

    # check single-quote in messages
    message = single_quote(message)

    # Add the mssg.
    db.add_message(user, friend, message)

    return chat(ip, "")

def receive_mssg(ip, sender):
    
    # Check if the user doesnt pick any friend.
    if sender == None:
        return chat(ip, "")

    # Get the username of the cur client.
    user = get_user_from_ip(ip)

    # Get the mssgs of the friend.
    mssg = db.get_message(sender, user)
    print(mssg)
    # Check if there's no mssg.
    if mssg == None:
        mssg = ""
        
    return chat(ip, mssg)

def get_ciphertext(username, sender):
    mssg = db.get_message(sender, username)

    # Check if there's no mssg.
    if mssg == None or sender == None:
        mssg = ""
    return mssg
    
# get public key of friend
def get_pks(ip):
    # Get the username of the cur client.
    user = get_user_from_ip(ip)

    # Get the friends' pk.
    pks = db.get_friend_pks(user)

    return pks

#-----------------------------------------------------------------------------
# Logout
#-----------------------------------------------------------------------------

def logout(ip):
    '''
        send
        sending messages.
    '''
    with open('logged_in.json', 'r') as openfile:
        # Reading from json file
        logged_in = json.load(openfile)

    # Check if not yet logged in.
    if ip not in logged_in:
        return page_view("not_logged_in")

    # Deleting the ip and the username from logged_in file.
    user = logged_in.pop(ip)
    json_object = json.dumps(logged_in, indent=4)

    with open('logged_in.json', 'w') as outfile:
        outfile.write(json_object)

    return page_view("success_out", name=user)

        

#-----------------------------------------------------------------------------
# test
#-----------------------------------------------------------------------------

def test():
    '''
        test
        for testing purpose only
    '''
    return page_view("test")

#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------

def register(mssg):
    '''
        whatever
        Returns the view for the whatever page
    '''
    return page_view("register", reg_mssg=mssg)


def register_create(username, password):

    # Check if the username is empty. 
    cond1 = username == None or len(username) == 0
    if cond1:
        return register("username is empty")

    # Check if the password is empty.
    cond2 = password == None or len(password) == 0
    if cond2:
        return register("password is empty")

    # Check if the username already exist.
    result = db.get_user(username)
    if result != None:
        return register("username already exists")

    # Creating the random salt and combine it with the pwd.
    salt = str(random.randint(0, 100))
    password = hash_info(password+salt)

    # Add the user.
    success = db.add_user(username, password, 'new', salt, 0)
    err_str = "register errors"

    if success == True:
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

def set_pk(user, pk):
    # convert pk-string to correct format to add to the db
    pk = single_quote(pk)

    username, pwd, salt = db.get_user_and_pwd(user)
    # print(username +' ' + pwd)

    db.delete_user(user)

    success = db.add_user(username, pwd, pk, salt, 0)

    if success == True:
        print(f"succeed adding pk to user {username}!")
    else:
        print(f"failed adding pk to user {username}")

#-----------------------------------------------------------------------------
# Friend
#-----------------------------------------------------------------------------
def friend(ip, a_mssg, r_mssg):
    
    user = get_user_from_ip(ip)
    if user == None:
        return page_view("not_logged_in")

    return page_view("friend", add_mssg=a_mssg, rm_mssg=r_mssg, username=user)

def ad_friend(name, ip):
    # Check if the input is empty.
    if name == None:
        return friend(ip, "input is empty", "")
    
    user = get_user_from_ip(ip)

    # Check if the input is not one of the users.
    result = db.get_user(name)
    if result == None:
        return friend(ip, "username input is invalid", "")

    # Check if the input is already friend with the user.
    result = db.is_friend(user, name)
    if result == True:
        return friend(ip, f"{name} is already friend", "")

    # Addind each other as friend.
    db.add_friend(user, name)
    db.add_friend(name, user)

    return friend(ip, f"{name} successfully added", "")

def rm_friend(name, ip):
    # Check if the input is empty.
    if name == None:
        return friend(ip, "", "input is empty")
    
    user = get_user_from_ip(ip)

    # Check if the input is not one of the users.
    result = db.get_user(name)
    if result == None:
        return friend(ip, "", "username input is invalid")

    # Check if the input is already friend with the user.
    result = db.is_friend(user, name)
    if result == False:
        return friend(ip, f"{name} is not a friend", "")

    # Removing both ways.
    db.delete_friend(user, name)
    db.delete_friend(name, user)

    return friend(ip, "", f"{name} successfully removed")    

#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)