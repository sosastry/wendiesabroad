#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import connSetup
import MySQLdb
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers
import imageUpload
import session
import logText
import uuid

loginButton = False

# we will add login capabilities!
# gets the data that the user entered into the form and processes it
def submitUser():
    form_data=cgi.FieldStorage()
   # print "form data: ",form_data
# checks whether the script has been called using the submit button
    if (form_data.getvalue('submit')):
      userData = []
      
      userData.append(cgi.escape(form_data.getfirst('name')))
      userData.append(cgi.escape(form_data.getfirst('email')))
      userData.append(cgi.escape(form_data.getfirst('password')))
      userData.append(cgi.escape(form_data.getfirst('year')))
      userData.append(form_data.getfirst('major'))
      userData.append(cgi.escape(form_data.getfirst('activities')))

      fileitem_prof = form_data['propic']
      fileitem_cover = form_data['cover']
      username = userData[1]
      conn = connSetup.connect(connSetup.dsn)

      if (profileComplete(userData)):
          if (userExists(conn,username)):
              print '<p style="color:red">An account already exists with this email address.</p>'
              print main()
              #print out form again with user input
          else:
              pid = insertUser(conn,userData)
              #upload profile picture
              imageUpload.process_file_upload(pid, fileitem_prof.filename, fileitem_prof.file,0,'profile')   
              #upload cover photo
              imageUpload.process_file_upload(pid, fileitem_cover.filename, fileitem_cover.file,0,'cover')
              print '<p style="color:red">Profile successfully created.</p>'
              print main()
      else:
          print main()
          print '<p style="color:red">Please fill out all fields.</p>'
          # print out form again with user input

    else:
        print main()

def userExists(conn,username):
    curs=conn.cursor(MySQLdb.cursors.DictCursor)
    data=(username,)
    curs.execute('SELECT username FROM creds WHERE username=%s',data)
    row=curs.fetchone()
    if row is None:
        return False
    else:
        return True
    
    # inserts data into review table
# TODO: check if user already exists
def insertUser(conn,userData):
  curs = conn.cursor(MySQLdb.cursors.DictCursor)
  email = userData[1] + "@wellesley.edu"
  salt = uuid.uuid4().hex
  user_data = (userData[0],email,userData[3],userData[4],userData[5],)

  curs.execute('insert into user(name,email,year,major,activities) values (%s,%s,%s,%s,%s)',user_data)
  curs.execute('select last_insert_id()')
  pid = curs.fetchone()['last_insert_id()']
  print 'insert user row id:',pid

  creds_data = (pid,salt,userData[1],userData[2],)
  curs.execute('INSERT into creds(pid, salt, username, password) values (%s, %s,  %s, %s)',creds_data)
  print 'insert creds for: ',userData[1]
  return pid

# tests whether user has entered in all fields in a review
def profileComplete(list):
  for item in list:
      if (item is ''):
          return False
  return True

# prints out the html template
def main():
    global loginButton
    data = {}
    data['login'] = logText.loginFormat(loginButton)
    tmpl =  file_contents('createprofile.html')
    return tmpl.format(**data)

# main method to perform data processing and print html template
if __name__== '__main__':
   global loginButton
   print "Content-Type: text/html\n"
   session.checkExistingSession()
   loginButton = session.isLogin()
   submitUser()


