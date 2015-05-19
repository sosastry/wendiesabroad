#!/usr/local/bin/python2.7
 
# Script to do a simple session
 
# Scott D. Anderson
# scott.anderson@acm.org
# April 2014
# wrote the functions to mimic PHP's session functions.
 
import os
import os.path
import sys
import cgi
import cgitb; cgitb.enable
 
import Cookie
import pickle
import cgi_utils_sda

# prints session header, so only header output, no debugging output

my_sess_dir = 'sessions/'
login = False
username =''

def isLogin():
    global login
    return login

def getUsername():
    global username, login
    if login: 
        return username
    else: 
        return ""

def setUsername(uname):
    global username
    username = uname

def checkExistingSession():
    global login
    global username
    sess_data = cgi_utils_sda.session_start(my_sess_dir)
    if sess_data['loggedIn'] == True: #already logged in
        setUsername(sess_data['username'])
        login = True
        print "Logged in: " + sess_data['username']

#creates session for new login
def createSession(username):
    sess_data = cgi_utils_sda.session_start(my_sess_dir)
    if sess_data['loggedIn'] == False: #new login
        sess_data['loggedIn']=True 
        sess_data['username']=username
        setUsername(username)
        # create new session file
        output = open(my_sess_dir+sess_data['sessid'],'w+')
        pickle.dump(sess_data,output,-1)
        output.close()
        login = True
        print "Welcome ",username,"!"
        os.system("./home.cgi")
        
    else: 
        print "Welcome back ",username,"!"
        os.system("./home.cgi")
