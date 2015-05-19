#!/usr/local/bin/python2.7

def loginFormat(login):
    if login:
        return '<li><a href="logout.cgi"><span class="glyphicon glyphicon-home"></span> Logout </a></li>'
    else: 
        return  '<li><a href="login.cgi"><span class="glyphicon glyphicon-log-in"></span> Login </a></li>'
