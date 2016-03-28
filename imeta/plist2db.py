#!/usr/bin/env python3

# Major top elements of "Library.xml", the Library export from iTunes, include:
# - Tracks (done)
# - Playlists
# - Playlist_Items: [Track_ID, ...]

import plistlib
import sqlite3
import os, sys, string, argparse, logging

song_keys = [
    'Album',
    'Artist',
    'Bit_Rate',
    'Comments',
    'Composer',
    'Date_Added',
    'Date_Modified',
    'Disc_Count',
    'Disc_Number',
    'File_Folder_Count',
    'Genre',
    'Kind',
    'Library_Folder_Count',
    'Location',
    'Name',
    'Normalization',
    'Persistent_ID',
    'Play_Count',
    'Play_Date',
    'Play_Date_UTC',
    'Rating',
    'Sample_Rate',
    'Size',
    'Total_Time',
    'Track_Count',
    'Track_ID',
    'Track_Number',
    'Track_Type',
    'Year',
]

pl_keys = [
    'Description',
    'Name',
    'Playlist_ID',
    'Playlist_Persistent_ID']

def createdb(c):
    c.execute('''CREATE TABLE songs 
    (
    Album TEXT,
    Artist TEXT,
    Bit_Rate INTEGER,
    Comments TEXT,
    Composer TEXT,
    Date_Added timestamp,
    Date_Modified timestamp,
    Disc_Count INTEGER,
    Disc_Number INTEGER,
    File_Folder_Count INTEGER,
    Genre TEXT,
    Kind TEXT,
    Library_Folder_Count INTEGER,
    Location TEXT,
    Name TEXT,
    Normalization INTEGER,
    Persistent_ID TEXT,
    Play_Count INTEGER,
    Play_Date INTEGER,
    Play_Date_UTC timestamp,
    Rating INTEGER,
    Sample_Rate INTEGER,
    Size INTEGER,
    Total_Time INTEGER,
    Track_Count INTEGER,
    Track_ID INTEGER primary key,
    Track_Number INTEGER,
    Track_Type TEXT,
    Year INTEGER
    )''')

    c.execute('''CREATE TABLE playlists
    (
    Description TEXT,
    Name TEXT,
    Playlist_ID INTEGER,
    Playlist_Persistent_ID TEXT
    )''')

    c.execute('''CREATE TABLE playlists_songs
    (
    Playlist_ID INTEGER, 
    Track_ID INTEGER
    )''')
    # END createdb()
             
def replace_space(attrs):
    '''For keys in dict ATTRS that contain blanks, add key replacing with underscore'''
    for k,v in attrs.items():
        if ' ' in k:
            attrs[k.replace(' ', '_')] = v
            attrs.pop(k)
            
def loaddb(plist_fp, dbfile):
    exists = os.path.exists(dbfile)
    conn = sqlite3.connect(dbfile,
                           detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    if not exists:
        createdb(c)

    pl = plistlib.load(plist_fp)

    # INSERT into  playlists, playlists_songs
    playlists = []
    pl_track_list = [] # (playlist_id, track_id)
    for attrs in pl['Playlists']:
        replace_space(attrs)
        #! print('DBG: Playlists={}'.format(attrs))
        playlists.append(tuple([attrs.get(k) for k in pl_keys if k != 'Playlist Items']))
        if 'Playlist Items' in attrs:
            for tid in [d['Track ID'] for d in attrs['Playlist Items']]:
                pl_track_list.append((attrs['Playlist ID'],tid))
    sql = ("INSERT INTO playlists({}) VALUES ({})"
           .format(', '.join(pl_keys),
                   ('?, '*len(pl_keys))[:-2],
           ))
    c.executemany(sql, playlists)
    c.executemany('INSERT into playlists_songs(Playlist_ID,         songs.append(tuple([attrs.get(k) for k in song_keys]))
    sql = ("INSERT INTO songs({}) VALUES ({})"
           .format(', '.join(song_keys),
                   ('?, '*len(song_keys))[:-2],
           ))
    c.executemany(sql, songs)
    #!c.execute("select * from songs limit 5")
    #!print('SONGS={}'.format(c.fetchall()))


    conn.commit()
    conn.close()


##############################################################################

def main_tt():
    cmd = 'MyProgram.py foo1 foo2'
    sys.argv = cmd.split()
    res = main()
    return res

def main():
    #!print('EXECUTING: {}\n\n'.format(' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        #!version='1.0.1',
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('library_plist',  help='Input file',
                        type=argparse.FileType('rb') )
    parser.add_argument('music_db',
                        help='SQLITE DB to contain song info', )
    parser.add_argument('-q', '--quality', help='Processing quality',
                        choices=['low','medium','high'], default='high')
    parser.add_argument('--loglevel',      help='Kind of diagnostic output',
                        choices = ['CRTICAL','ERROR','WARNING','INFO','DEBUG'],
                        default='WARNING',
                        )
    args = parser.parse_args()
    #!args.outfile.close()
    #!args.outfile = args.outfile.name

    #!print 'My args=',args
    #!print 'infile=',args.infile


    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel) 
    logging.basicConfig(level = log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M'
                        )
    logging.debug('Debug output is enabled!!!')


    loaddb(args.library_plist, args.music_db)

if __name__ == '__main__':
    main()
