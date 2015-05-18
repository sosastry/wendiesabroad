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
 
import Cookie
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers
 
 
#Validate username and password
def validateUser():
    form_data = cgi.FieldStorage()

    if ('username' in form_data) and ('password' in form_data):
        pword = form_data.getfirst('password')
        username = form_data.getfirst('username')

        if validPassword(username,pword):
            print "Success"
	    print "Sonali"
            session.main()
    else:
        print "Please enter both username and password"

def validPassword(username,password):     
    conn = connSetup.connect(connSetup.dsn)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
 
    data = (username,)
    curs.execute('select * from creds where username=%s',data)
    row = curs.fetchone()
    
    if row is None:
        print "Please enter valid username"
        return False
    
    databasePwd = row['password']
    
    if (password == databasePwd):
        print 'Thanks! Hello world!'
        return True
    else:
        print "incorrect password"
 
if __name__ == '__main__':
    print "Content-Type: text/html\n"
    tmpl = file_contents('home.html')
    print tmpl
    validateUser()
    
