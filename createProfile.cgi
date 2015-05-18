#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import connSetup
import MySQLdb
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers
import imageUpload
import session

# we will add login capabilities!
# gets the data that the user entered into the form and processes it
def submitUser():
    form_data=cgi.FieldStorage()
    # checks whether the script has been called using the submit button
    if (form_data.getvalue('submit')):
      userData = []

      userData.append(cgi.escape(form_data.getfirst('name')))
      userData.append(cgi.escape(form_data.getfirst('year')))
      userData.append(form_data.getfirst('major'))
      userData.append(cgi.escape(form_data.getfirst('email')))
      userData.append(cgi.escape(form_data.getfirst('activities')))

      fileitem_prof = form_data['propic']
      fileitem_cover = form_data['cover']

      if (profileComplete(userData)):
          pid = insertUser(connSetup.connect(connSetup.dsn),userData)
          #upload profile picture
          imageUpload.process_file_upload(pid, fileitem_prof.filename, fileitem_prof.file,0,'profile')   
          #upload cover photo
          imageUpload.process_file_upload(pid, fileitem_cover.filename, fileitem_cover.file,0,'cover')
          print main()
          print '<p style="color:red">Profile successfully created.</p>'
          
      else:
          print main()
          print '<p style="color:red">Please fill out all fields.</p>'
          # print out form again with user input

    else:
        print main()

# inserts data into review table
# TODO: check if user already exists
def insertUser(conn,userData):
  curs = conn.cursor(MySQLdb.cursors.DictCursor)
  data = (userData[0],userData[1],userData[2],userData[3],userData[4],)
  curs.execute('insert into user(name,year,major,email,activities) values (%s,%s,%s,%s,%s)',data)

  
  curs.execute('select last_insert_id()')
  pid = curs.fetchone()['last_insert_id()']
  print 'insert user row id:',pid
  return pid

# tests whether user has entered in all fields in a review
def profileComplete(list):
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
   session.checkExistingSession()
   submitUser()
   #print main()


