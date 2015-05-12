#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import connSetup
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers

# gets the data that the user entered into the form and processes it
def submitReview():
    form_data=cgi.FieldStorage()
    print form_data
    # checks whether the script has been called using the submit button
    if (form_data.getvalue('submit')):
      reviewData = []

      reviewData.append(form_data.getfirst('title'))
      reviewData.append(form_data.getfirst('university'))
      reviewData.append(form_data.getfirst('rating'))
      reviewData.append(form_data.getfirst('review_text'))
      reviewData.append(form_data.getfirst('photo'))
      reviewData.append(form_data.getvalue('author'))

      if (reviewComplete(reviewData)): #confirms that all fields are filled out
        insertReview(connSetup.connect(connSetup.dsn),reviewData)
      else:
        print '<p style="color:red">Please fill out all fields.</p>'

# inserts data into review table
def insertReview(conn,reviewData):
  curs = conn.cursor(MySQLdb.cursors.DictCursor)
  data= (reviewData[5],reviewData[1],reviewData[5],reviewData[0],reviewData[3],reviewData[2],)
  curs.execute('insert into review(pid,uid,name,title,reviewText,rating) values (%s,%s,%s,%s,%s,%s)',data)
  print "Successfully inserted review with title: " + reviewData[0]

# tests whether user has entered in all fields in a review
def reviewComplete(list):
  for item in list:
    if (item is None):
      return False
  return True

#gets list of users from database
def getUsers():

    formatString = "<option value='{pid}'>{name}</option>"
    resultString = ""
    results = {}
    conn = connSetup.connect(connSetup.dsn)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from user')

    row = curs.fetchone()

    while row is not None:
        resultString += formatString.format(**row)
        row = curs.fetchone()
    
    results['users'] = resultString
    return results

# prints out the html template
def main():
    tmpl =  file_contents('writereview.html')
    
    #get list of users in user table
    users = getUsers()
    print tmpl.format(**users)

# main method to perform data processing and print html template
if __name__== '__main__':
   print "Content-Type: text/html\n"
   submitReview()
   print main()


