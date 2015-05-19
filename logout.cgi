#!/usr/local/bin/python2.7

import session
import os
import cgi_utils_sda

dir = "sessions/"

#logs user out and takes them back to page they were on prior to logout
def logout():
    sessid = cgi_utils_sda.session_id() #grab current session id
    sess_data = cgi_utils_sda.session_start(dir)
    os.remove(dir+sessid)
    print 'Logged out: ' + sess_data['username']

    os.system("./home.cgi")

    '''redirectLink = os.environ['HTTP_REFERER']

    redirectLink = redirectLink.split('http://cs.wellesley.edu/~wabroad/cgi-bin/wendiesabroad/',1)

    #special cases for university & user profile pages
    if ('.cgi?' not in redirectLink[1]):
        redirectLink = "./"+redirectLink[1]
    else: 
        print 'false'
        newSplit = redirectLink[1].split('?',1) #userprofile.cgi
        print newSplit[0] + "HELLO \n <br>"
        print newSplit[1]
        getFormValue = newSplit[1].split('=',1) #pid, 3
        print getFormValue[1]
        redirectLink = "./" + newSplit[0] + ' ' + "'" + getFormValue[0] + '=' + getFormValue[1] + "'"
        redirectLink = "./"+newSplit[0]
        print "NEW REDIRECT\n: " + redirectLink 
       
    os.system(redirectLink)'''


if __name__ == '__main__':
    print "Content-Type: text/html\n"
    logout()



    
