#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import connSetup
import cgi_utils_sda
from cgi_utils_sda import file_contents,print_headers

# gets the data that the user entered into the form and processes it
def getSearchQuery():
    form_data=cgi.FieldStorage()

    # checks whether the script has been called using the submit button
    if (form_data.getvalue('searchQuery')):
      searchQuery = form_data.getfirst('searchQuery')
      searchType = form_data.getfirst('searchby')
      if ((searchQuery is not None) and (searchType is not '0')):
        try:
          searchDatabase(connSetup.connect(connSetup.dsn),cgi.escape(searchQuery),searchType)
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
    result = {}
    resultString = ""
    uniFormat = '<a href="university.cgi?uni={uid}" class="testing">{name}</a><br>'
    
    if searchType == '1':  #country
      data=(searchQuery,)
      curs.execute('select * from university join country where university.country = country.cid and country.name like %s',data)
      row = curs.fetchone()
      if row is None:
          resultString += "Your search did not return any results."
      else:
          while row is not None:
              resultString += uniFormat.format(**row)
              row = curs.fetchone()
    elif searchType == "2": #university
      data=(searchQuery,)
      curs.execute('select * from university where name like %s', data)
      row=curs.fetchone()
      if row is None:
          resultString += "Your search did not return any results."
      else: 
          while row is not None:
              resultString += uniFormat.format(**row)
              row = curs.fetchone()
    elif searchType == "3": #people
        data=(searchQuery,searchQuery,searchQuery,)
        curs.execute('select * from user where name like %s OR major like %s OR activities like %s', data)
        row=curs.fetchone()
        if row is None:
            resultString += "Your search did not return any results."
        else:
            while row is not None:
                resultString  += ('<div class="testing" value={pid}>{name}</div>').format(**row)
                row = curs.fetchone()
    result['results'] = resultString 
    print main().format(**result)

# prints out the html template
def main():
    tmpl =  file_contents('searchresults.html')
    return tmpl

# main method to perform data processing and print html template
if __name__== '__main__':
   print "Content-Type: text/html\n"
   getSearchQuery() 


