#!/usr/local/bin/python2.7
 
# Script to do a simple session
 
# Scott D. Anderson
# scott.anderson@acm.org
# April 2014
# wrote the functions to mimic PHP's session functions.

import cgi
import cgitb; cgitb.enable
import connSetup
import session
import MySQLdb
import hashlib
import uuid
 
import Cookie
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers
 
 
#Validate username and password
def validateUser(form_data):
    #print "Form data: ",form_data
    username = form_data.getfirst('username')
    password = form_data.getfirst('password')
    #print "Username: ",username
    #print "Password: ", password
    if (username != '') and (password != ''):
	
        if validPassword(username,password):
            session.createSession(username)
    else:
        print "Please enter both username and password"
        printTmpl()

def validPassword(username,password):     
    conn = connSetup.connect(connSetup.dsn)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
 
    data = (username,)
    curs.execute('select * from creds where username=%s',data)
    row = curs.fetchone()
    
    if row is None:
        print "Please enter a  valid username and password"
        printTmpl()
        return False

    #retrieve the salt from the database
    salt = row['salt']
    hashed_password=hashlib.sha512(password+salt).hexdigest()
    databasePwd = row['password']

    databasePwd = hashlib.sha512(databasePwd+salt).hexdigest()
    
    if (hashed_password == databasePwd):
        return True
    else:
        print "Please enter a valid username and password"
        printTmpl()

def printTmpl():
    tmpl = file_contents('login.html')
    print tmpl

if __name__ == '__main__':
    print "Content-Type: text/html\n"
    form_data = cgi.FieldStorage()
    
    if (form_data.getvalue('submit')):
       validateUser(form_data)       
    else:
        printTmpl()
    
