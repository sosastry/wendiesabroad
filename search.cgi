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
def getSearchQuery():
    form_data=cgi.FieldStorage()

    # checks whether the script has been called using the submit button
    if (form_data.getvalue('submit')):

      searchQuery = form_data.getfirst('searchQuery')
      searchType = form_data.getfirst('searchby')
      if ((searchQuery is not None) and (searchType is not '0')):
        try:
          searchDatabase(connect(dsn),cgi.escape(searchQuery),searchType)
        except ValueError:
          print 'Connection failed'
      else:
        if (searchQuery is None):
          print 'Please enter a search term <br>'
        if (searchType =='0'):
          print 'Please choose a search category'

#searches the database of the given query
def searchDatabase(conn,searchQuery,searchType):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    searchQuery = '%' + searchQuery + '%'
    data=(searchQuery,)
    result = []
    
    if searchType == '1':  #country
      data=(searchQuery,)
      #curs.execute('select university.name from university join country where university.country = country.cid and country.name like %s',data)
      curs.execute('select * from university join country where university.country = country.cid and country.name like %s',data)
      row = curs.fetchone()
    elif searchType == "2": #university
      data=(searchQuery,)
      curs.execute('select * from university where name like %s', data)
      row=curs.fetchone()
    elif searchType == "3": #people
        data=(searchQuery,searchQuery,searchQuery,)
        curs.execute('select * from user where name like %s OR major like %s OR activities like %s', data)
        row=curs.fetchone()
    if row is None:
      print "Your search did not return any results."
    while row is not None:
        result.append('<div class="testing" value={uid} onclick="test()">{name}</div>'.format(**row)) # need to change uid to pid for user
        row = curs.fetchone()
    for i in range(len(result)):
      print result[i]

def test():
    print hello

# prints out the html template
def main():
    tmpl =  file_contents('search.html')
    return tmpl

# main method to perform data processing and print html template
if __name__== '__main__':
   print "Content-Type: text/html\n"
   print main()
   getSearchQuery() 
   print "</td></tr></table></body></html>"


