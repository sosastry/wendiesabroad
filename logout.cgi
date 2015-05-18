#!/usr/local/bin/python2.7

import session
import os
import cgi_utils_sda

dir = "sessions/"

def logout():
    sessid = cgi_utils_sda.session_id() #grab current session id
    sess_data = cgi_utils_sda.session_start(dir)
    os.remove(dir+sessid)
    print 'Logged out: ' + sess_data['username']

    redirectLink = os.environ['HTTP_REFERER']
    hello = redirectLink.split('http://cs.wellesley.edu/~wabroad/cgi-bin/wendiesabroad/',1)
    
    string = "./"+hello[1]
    os.system(string)

if __name__ == '__main__':
    logout()


    
