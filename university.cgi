#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import connSetup
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers
import session

# prints out the html template
def main():
    tmpl =  file_contents('university.html')
    return tmpl

def getUniInfo():
    form_data=cgi.FieldStorage()

    if (form_data.getvalue('uni')):
        uid = form_data.getfirst('uni')
        conn = connSetup.connect(connSetup.dsn)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        data = (uid,)
        
        curs.execute('select * from university where uid=%s',data)
        row = curs.fetchone()
	cid = row.get('country')

	data = (cid,)
	curs.execute('select name from country where cid=%s',data)
	row2 = curs.fetchone()

	row['countryName'] = row2.get('name')

	# MAKE CODE MORE MODULAR (ANOTHER FUNCTION)
#wendies at the uni
        wendiesList=[]
        data=(uid,)
        curs.execute('select user.pid, user.name from user where pid in (select pid from review where uid = %s)',data)

        peopleRow = curs.fetchone()

        while peopleRow is not None:
            wendiesList.append(peopleRow)
            peopleRow = curs.fetchone()

        personFormat = "<a href='userprofile.cgi?pid={pid}'>{name}</a><br>"
        peopleString = ""

        for r in wendiesList:
            peopleString += personFormat.format(**r)

        row['peopleString'] = peopleString

#uni reviews
        reviewResults=[]
        data=(uid,)
        curs.execute('select * from review where uid=%s',data)

        reviewRow = curs.fetchone()

        while reviewRow is not None:
            reviewResults.append(reviewRow)
            reviewRow = curs.fetchone()

        revFormat = "<div class='review'><b>{title}</b><br>'{reviewText}' by {name}</div><br>"
        reviewString = ""

        for r in reviewResults:
            reviewString += revFormat.format(**r)

        row['resultString'] = reviewString

        tmpl = file_contents('university.html')
        print tmpl.format(**row)

# main method to perform data processing and print html template
if __name__== '__main__':
   print "Content-Type: text/html\n"
   session.checkExistingSession()
   getUniInfo()
