'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, error, request, static_file

import model
import time

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

#----------------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    return model.login_form(ip, "")

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Get the username and the password.
    username = request.forms.get('username')
    password = request.forms.get('password')

    # Get client's ip.
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    # Call the appropriate method
    return model.login_check(username, password, ip)

#-----------------------------------------------------------------------------

# Register
@get('/register')
def get_register():
    '''
        get_register
        
        Serves the whatever page
    '''
    return model.register("")

#-----------------------------------------------------------------------------

# Attempt the register

@post('/register')
def post_register():
    '''
        post_register
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Get the username and the password.
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.register_create(username, password)

#-----------------------------------------------------------------------------

@post('/getkey')
def get_key():
    # get public key
    received = request.json
    user = received['username']
    public_key = received['pub_key']
    return model.set_pk(user, public_key)

    # return model.store_pk(username, public_key)

#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()

#-----------------------------------------------------------------------------

@get('/chat')
def get_chat():
    '''
        get_chat
        
        Serves the chat page
    '''
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    return model.chat(ip, "")

#-----------------------------------------------------------------------------

# Receuve the message
@post('/chat')
def post_chat():
    '''
        Receive the message.
    '''
    # Check whether sending or receiving.
    button = request.forms.get('button')  # get value from the name
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    if button == 'send':
        friend = request.forms.get("send_person")
        message = request.forms.get("send_message")
        print("post_chat: friend:", friend, "| message:", message)

        return model.chat(ip, "")

    elif button == 'receive':
        sender = request.forms.get('rec_person')
        print(f"rec_person: {sender}")
        
        return model.receive_mssg(ip, sender) 


@post('/get_ciphertext')
def get_ciphertext():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    # get encrypted message + friend's name from encode message.js
    received = request.json
    print("get_ciphertext: ")
    print(received)

    if received == None:
        print("no message is sent")
        return model.chat(ip, "")

    friend = received['friend']
    cipher_message = received['send_message']

    # print("get_cipher: friend:", friend)
    # print(cipher_message)

    return model.create_chat(ip, friend, cipher_message)

#-----------------------------------------------------------------------------

@get('/retrieve_pks')
def retrieve_pks():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    pks = model.get_pks(ip)
    return pks

#-----------------------------------------------------------------------------

@get('/get_username')
def get_username():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    data = {}
    username = model.get_user_from_ip(ip)

    data["user"] = username
 
    return data

#-----------------------------------------------------------------------------
@post('/request_ciphertext')
def request_ciphertext():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    sender = request.json
    print("sender: ")
    print(sender)

    if sender == None:
        return model.chat(ip, "")
    elif sender["sender"] == None:
        return model.chat(ip, "")

    data = {}
    username = model.get_user_from_ip(ip)
    message = model.get_ciphertext(username, sender["sender"])

    if message == "":
        return model.chat(ip, "")

    data["message"] = message

    # print(data)
    return data

#-----------------------------------------------------------------------------------

@get('/logout')
def get_logout():
    '''
        get_logout
        
        Serves the logout page
    '''

    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    return model.logout(ip)

#-----------------------------------------------------------------------------
# Friend
#-----------------------------------------------------------------------------

@get('/friend')
def get_friend():
    '''
        get_send
        
        Serves the chat page
    '''
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    return model.friend(ip, "", "")

#-----------------------------------------------------------------------------

@post('/friend')
def post_friend():
    '''
        get_send
        
        Serves the chat page
    '''
    button = request.forms.get('button')  # get value from the name
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or \
        request.environ.get('REMOTE_ADDR')

    if button == 'add':
        friend = request.forms.get("username")
        #print("add:", friend)
        return model.ad_friend(friend, ip)

    elif button == 'remove':
        friend = request.forms.get('username')
        #print("remove", friend)
        return model.rm_friend(friend, ip)

#-----------------------------------------------------------------------------

@get('/test')
def get_test():
    '''
        page view for testing purpose only
    '''
    return model.test()

#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)
