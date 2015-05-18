
#!/usr/local/bin/python2.7
 
# Script to do a simple session
 
# Scott D. Anderson
# scott.anderson@acm.org
# April 2014
# wrote the functions to mimic PHP's session functions.
 
import os
import os.path
import sys
import cgi
import cgitb; cgitb.enable
import connSetup
 
import Cookie
import cgi_utils_sda
 
addToCartButton = 'add to cart'
showCartButton = 'show cart'
itemName = 'itemid'
 
def addToCart(item):
    global cart
    cart[item] += 1
    return "<p>Thanks for ordering <strong>"+item+"</strong>."
 
def showCart():
    global cart;
    val = "<p>Your cart has \n<ul>"
    for k,v in cart.iteritems():
        val += "<li>{value} glasses of {key}\n".format(key=k,value=v)
    val += "</ul>\n"
    return val
 
 #Validate username and password
def validateUser():
    form_data = cgi.FieldStorage()

    if (username in form_data) and (password in form_data):
        pword = form_data.getfirst('password')
        username = form_data.getfirst('username')

        if validPassword(username,pword):
            print "Success"
    else:
        print "Please enter both username and password"

def validPassword(username,password):     
    conn = connSetup.connect(connSetup.dsn)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
 
    data = (username,)
    curs.execute('select * from creds where username=%s',data)
    row = curs.fetchone()
    
    if row is None:
        print "Please enter valid username"
        return false
    
    databasePwd = row[password]
    
    if password = database.password:
        print 'Thanks! Hello world!'
        return true
    else:
        print "incorrect password"

def main():
    my_sess_dir = 'sessions/'
    print 'Content-type: text/html'
    sess_data = cgi_utils_sda.session_start(my_sess_dir)
 
    if 'username' in sess_data:
        user = sess_data['username']
    else:
        user = {'beer': 0, 'wine': 0, 'soda': 0}
 
    self = sys.argv[0]
 
    msg = ''
    form_data = cgi.FieldStorage()
    if 'submit' in form_data:
        action=form_data.getfirst('login')
        
            msg = addToCart(form_data.getfirst(itemName))
        elif action == showCartButton:
            msg = showCart()
        else:
            msg = "<p>Error: invalid action: $action";
 
if __name__ == '__main__':
    #main()
    validateUser()
    
