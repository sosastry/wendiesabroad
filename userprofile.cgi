#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import connSetup
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers

# prints out the html template
def main():
    tmpl =  file_contents('userprofile.html')
    return tmpl

def getUserInfo():
    form_data=cgi.FieldStorage()

    if (form_data.getvalue('pid')):
        pid = form_data.getfirst('pid')
        conn = connSetup.connect(connSetup.dsn)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        data = (pid,)
        
        curs.execute('select * from user where pid=%s',data)
        row = curs.fetchone()

	# MAKE CODE MORE MODULAR (ANOTHER FUNCTION)
        userReviews=[]
        data=(pid,)
        curs.execute('select * from review where pid=%s',data)

        reviewRow = curs.fetchone()

        while reviewRow is not None:
            userReviews.append(reviewRow)
            reviewRow = curs.fetchone()

        revFormat = "<div class='review'><b>{title}</b> by {name}</div>'{reviewText}'<br><br>"
        reviewString = ""

        for r in userReviews:
            reviewString += revFormat.format(**r)

        row['resultString'] = reviewString

        tmpl = file_contents('userprofile.html')
        print tmpl.format(**row)

# main method to perform data processing and print html template
if __name__== '__main__':
   print "Content-Type: text/html\n"
   # print main()
   getUserInfo()
