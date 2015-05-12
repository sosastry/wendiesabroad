import MySQLdb 

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
