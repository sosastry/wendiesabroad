#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import session
from cgi_utils_sda import file_contents,print_headers
import logText

loginButton = False

# prints out the html template
def main():
    global loginButton
    format = {}
    format['login'] = logText.loginFormat(loginButton)
    tmpl =  file_contents('home.html').format(**format)
    print tmpl

if __name__== '__main__':
   global loginButton
   print "Content-Type: text/html\n"
   session.checkExistingSession()
   loginButton = session.isLogin()
   main()
