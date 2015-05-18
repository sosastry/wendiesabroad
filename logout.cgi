#!/usr/local/bin/python2.7

import session
import os
import cgi_utils_sda

dir = "sessions/"

def logout():
    sessid = cgi_utils_sda.session_id() #grab current session id
    sess_data = cgi_utils_sda.session_start(dir)
    print sess_data
    os.remove(dir+sessid)
    print 'Logged out: ' + sess_data['username']
    print os.environ['HTTP_REFERER']

if __name__ == '__main__':
    print "Content-Type: text/html\n"
    logout()


    
