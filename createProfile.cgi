#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers

# sets database information prior to connection
dsn= {
'username':'wabroad',
'password':'s1ai7tzJLK1slY0',
'database':'wabroad_db',
'hostname':'localhost'
}

the_database_connection = False

# connects to the database and returns the connection to that database
def connect(dsn):
    global the_database_connection
    if not the_database_connection:
        try:
            the_database_connection = MySQLdb.connect( host=dsn['hostname'],
                                                       user=dsn['username'],
                                                       passwd=dsn['password'],
                                                       db=dsn['database'])
           
            the_database_connection.autocommit(True)
        except MySQLdb.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %
                   (e.args[0], e.args[1]))
    return the_database_connection

# gets the data that the user entered into the form and processes it
def submitUser():
    form_data=cgi.FieldStorage()

    # checks whether the script has been called using the submit button
    if (form_data.getvalue('submit')):
      reviewData = []

      reviewData.append(cgi.escape(form_data.getfirst('name')))
      reviewData.append(cgi.escape(form_data.getfirst('year')))
      reviewData.append(form_data.getfirst('major'))
      reviewData.append(cgi.escape(form_data.getfirst('email')))
      reviewData.append(cgi.escape(form_data.getfirst('activities')))

      if (reviewComplete(reviewData)):
        insertReview(connect(dsn),reviewData)
      else:
        print main()
        print '<p style="color:red">Please fill out all fields.</p>'
        # print out form again with user input

# inserts data into review table
# TODO: check if user already exists
def insertReview(conn,reviewData):
  curs = conn.cursor(MySQLdb.cursors.DictCursor)
  data = (reviewData[0],reviewData[1],reviewData[2],reviewData[3],reviewData[4],)
  curs.execute('insert into user(name,year,major,email,activities) values (%s,%s,%s,%s,%s)',data)
  print main()
  print '<p style="color:red">Profile successfully created.</p>'

# tests whether user has entered in all fields in a review
def reviewComplete(list):
  for item in list:
    if (item is None):
      return False
  return True

# prints out the html template
def main():
    tmpl =  file_contents('createprofile.html')
    return tmpl

# main method to perform data processing and print html template
if __name__== '__main__':
   print "Content-Type: text/html\n"
   submitUser()
   #print main()


