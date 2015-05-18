
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
import cgi_utils_sda

def main():
    print "HELLO"
    my_sess_dir = 'session/'
    #print 'Content-type: text/html'
    sess_data = cgi_utils_sda.session_start(my_sess_dir)

    print "HELLO!!!!!!!!!"
    print sess_data
 
    if 'pid' in sess_data:
        pid = sess_data['pid']
    else:
        pid = 0 #just browsing, not logged in

    form_data = cgi.FieldStorage()
    if 'submit' in form_data:
        action=form_data.getfirst('submit')
        
    # Whole response

 
if __name__ == '__main__':
    main()
    
