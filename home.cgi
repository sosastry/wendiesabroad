#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import session
from cgi_utils_sda import file_contents,print_headers

# prints out the html template
def main():
    tmpl =  file_contents('home.html')
    print tmpl

if __name__== '__main__':
   print "Content-Type: text/html\n"
   session.checkExistingSession()
   main()
