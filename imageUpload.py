#!/usr/local/bin/python2.7

import os
import sys
import cgi
import re
import MySQLdb
from subprocess import call

import connSetup
import cgi_utils_sda

DEST_DIR = '/students/wabroad/public_html/cgi-bin/wendiesabroad/images/' #pwd
DEST_URL = '/~wabroad/cgi-bin/wendiesabroad/images/'
IN_DB    = False                # false means store in dest_dir
MAX_FILE_SIZE = 2000000          # 2 MB

# ================================================================

database_connection = None
cursor = None


def cursor():
    database_connection = connSetup.connect(connSetup.dsn)
    cursor = database_connection.cursor(MySQLdb.cursors.DictCursor) # results as dictionaries
    return cursor

def generate_actor_menu(cursor):
    '''Returns an HTML menu of all actors in the WMDB'''
    cursor.execute('SELECT nm,name FROM person ORDER BY name')
    menu = '<select name="menu-nm">\n'
    for row in cursor.fetchall():
        menu += '<option value="{nm}">{name} ({nm})</option>\n'.format(
            nm=row['nm'],name=row['name'])
    menu += '</select>\n'
    return menu

def filesize(absfilename):
    '''Returns the length of a file in bytes'''
    stat = os.stat(absfilename)
    return stat.st_size

def check_integer(string,default):
    '''Converts string to an integer if it's all digits, otherwise
returns default'''
    if re.search('^\\d+$',string):
        try:
            return int(string)
        except:
            return default
    else:
        return default

def store_data_in_database(nm,client_filename,file_data,cursor):
    '''inserts or updates picture blob for this actor'''
    try:
        rows_mod = cursor.execute('''
INSERT INTO picblob(nm,pic) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE pic=%s
''',
                                  (nm,file_data,file_data))
    except Exception as e:
        print e
        return 'Failure to store picture data into database: '+str(e)
    if rows_mod != 1:
        return ('Failure to store picture data into database; '+
                'rows modified is '+
                str(rows_mod))
    return 'Successfully uploaded picture data for nm='+str(nm)


# generates the destination file and url strings based on which type of photo is
# being uploaded (review photo, profile picture or cover photo)
def getDestFile(callFrom, pid, rid):
    locations = {}
    
    if (callFrom == 'review'):
        dirString = 'reviews/' + str(rid) + '-' + str(pid) + '-1.jpg'
        locations['row_id'] = rid
        locations['query'] = "UPDATE review SET photo=%s WHERE rid=%s"
    elif (callFrom == 'cover'):
        dirString = 'users/' + str(pid) + '-cov.jpg'
        locations['row_id'] = pid
        locations['query'] = "UPDATE user SET cover=%s WHERE pid=%s"
    else:  #profile picture
        dirString = 'users/' + str(pid) + '-prof.jpg'
        locations['row_id'] = pid
        locations['query'] = "UPDATE user SET profPic=%s WHERE pid=%s"

    locations['dest_file'] = DEST_DIR + dirString
    locations['dest_url'] = DEST_URL + dirString
    locations['dirString'] = 'images/' + dirString

    print locations

    return locations

def store_data_in_filesystem_optimistic(pid,client_filename,file_data,rid, callFrom):
    '''Stores data in the filesystem as nm.jpg without checking for errors'''

    locations = getDestFile(callFrom, pid, rid)

    dest_file = locations['dest_file']

    stream = open(dest_file,'wb')
    stream.write(file_data)
    os.chmod(dest_file,0644)
    ## Now, record the URL in the database
    ## inserts or updates picture blob for this actor
    #url = DEST_URL + str(pid) + '.jpg'

    url = locations['dest_url']
    row_id = locations['row_id']
    query = locations ['query']

    curs = cursor()

    file_name = locations['dirString']
    data = (file_name,row_id,)

    rows_mod = curs.execute(query, data)
    
    return ('''
The picture file {fromfile} was uploaded successfully as {tofile}
<a href="{url}"><img src="{url}"></a> '''.format(fromfile=client_filename,
                                           tofile=client_filename,
                                                 url=url))

def store_data_in_filesystem(pid,client_filename,file_data,rid, callFrom):
    '''Stores data in the filesystem as nm.jpg in an exception handler'''
    dest_file = DEST_DIR + str(pid) + '.jpg'
    #print 'dest_file : ', dest_file
    try:
        return store_data_in_filesystem_optimistic(pid,client_filename,file_data,rid,callFrom)
    except Exception as e:
        return 'Failure to create output file %s: %s' % (dest_file,e)
    

def store_data_in_filesystem_paranoid(nm,client_filename,file_data,cursor):
    '''Stores data checking for lots of errors'''
    dest_file = DEST_DIR + str(nm) + '.jpg'
    try:
        stream = open(dest_file,'wb')
    except Exception as e:
        return 'Failure to open output file %s: %s' % (dest_file,e)
    try:
        stream.write(file_data)
    except Exception as e:
        return 'Failure to copy file data to %s: %s' % (dest_file,e)
    try:
        os.chmod(dest_file,0644)
    except Exception as e:
        return 'Failure to make file %s world-readable: %s' % (dest_file,e)

    ## Now, record the URL in the database
    url = DEST_URL + str(nm) + '.jpg'
    try:
        ## inserts or updates picture blob for this actor
        rows_mod = cursor.execute('''
INSERT INTO picfile(nm,url) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE url=%s
''',
                                  (nm,url,url))
    except Exception as e:
        print e
        return 'Failure to store picture URL in database: '+str(e)
    if rows_mod != 1:
        return ('Failure to store picture URL in database; '+
                'rows modified is '+
                str(rows_mod))
    return ('The picture file %s was uploaded successfully as %s (%s) ' %
            (client_filename,dest_file,url))


def process_file_upload(authorid,client_filename,local_file,rid,callFrom):
    
    ## Test if the file was uploaded
    if not client_filename:
        return 'No file uploaded (yet)'
        
    file_data = local_file.read()
    ## Double check whether the file upload is too big
    if len(file_data) > MAX_FILE_SIZE:
        return 'Uploaded file is too big: '+str(len(file_data))

    ## Get the pid (authorid), which we will either use as a DB key or a filename        
    return store_data_in_filesystem(authorid,client_filename,file_data,rid, callFrom)
