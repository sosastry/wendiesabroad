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

def main(pid):
    my_sess_dir = 'sessions/'
    print 'Content-type: text/html'
    sess_data = cgi_utils_sda.session_start(my_sess_dir)
    if sess_data['loggedIn'] == False: #new login
        # print "logged in false"
        # create new session file
        sess_data['loggedIn']=pid 
        
        output = open(my_sess_dir+sess_data['sessid'],'w+')
        pickle.dump(sess_data,output,-1)
        output.close()
        
if __name__ == '__main__':
    main(pid)
    
