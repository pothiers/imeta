from pprint import pprint
import plistlib
pl = plistlib.load(open('Library-10-20-2015.xml', 'rb'))
# BIG pprint(pl)

[p['Name'] for p in pl['Playlists']]
# =>
['Library', 'Music', 'Movies', 'TV Shows', 'Podcasts', 'iTunes\xa0U', 'Audiobooks', 'Tones', 'Purchased', 'Purchased on frog pad 10-15-10', 'DEBUG', 'AAC', 'Protected', 'favorites', 'favorite albums 3gb', 'favorite albums 5gb', 'favorite albums 8gb', 'favorite albums 600mb', 'favorite albums 900mb', 'favorite artist 1gb', 'favorite artist 3gb', 'favorite artist 300mb', 'favorite artist 600mb', 'new stuff', 'top 3gb', 'Albums, favorites', 'Artists, favorites', 'fav 3gb', '90’s Music', 'ALL', 'Classical Music', 'Deva Premal, all', 'purchased', 'Recently Added', 'Recently Played', 'ringtone-from-songs', 'Rock', 'sleep', 'sleep, 300mb', 'sleep, 500mb', 'Spoken', 'Top 25 Most Played', 'Top Rated', 'Unrated', 'bawdy', 'bought 4-23-2011', 'cp-fav', 'dentist', 'geek', 'hacking', 'hike', 'iTunes Artwork Screen Saver', 'Oscar Brand', 'river', 'romance', 'sailing', 'swim', 'Voice Memos']

# Find songs in playlist 'hacking'
[p  for p in pl['Playlists'] if p.get('Name') == 'hacking'][0]
{'All Items': True,
 'Description': '',
 'Name': 'hacking',
 'Playlist ID': 81438,
 'Playlist Items': [{'Track ID': 17451},
                    {'Track ID': 15447},
                    {'Track ID': 15449},
                    {'Track ID': 15451}],
 'Playlist Persistent ID': '2216D24E0458F2DD'}

# Look up details of track from playlist
pl['Tracks']['17451']['Name']
'First of May'

# List all Track IDs in playlist 'hacking'
pids = [q['Track ID'] for q in [p  for p in pl['Playlists'] if p.get('Name') == 'hacking'][0]['Playlist Items']]

# names of songs in playlist
[pl['Tracks'][str(pid)]['Name'] for pid in pids]
['First of May', 'Code Monkey', 'Mandelbrot Set', 'That Spells DNA']

# Number of tracks that are checked (not "disabled")
len(([pl['Tracks'][k]['Name'] for k in pl['Tracks'].keys() if not pl['Tracks'][k].get('Disabled', False)]))
8989


# >>> pl.keys()
# dict_keys(['Major Version', 'Tracks', 'Date', 'Application Version', 'Music Folder', 'Playlists', 'Show Content Ratings', 'Library Persistent ID', 'Minor Version', 'Features'])
# >>> pl['Major Version']
# 1
# >>> pl['Date']
# datetime.datetime(2015, 10, 30, 17, 45, 8)
# >>> pl['Application Version']
# '12.3.1.23'
# >>> pl['Music Folder']
# 'file:///Volumes/External%20Data/Shared/music/'
# >>> 


# pprint(list(pl['Tracks'].items())[0])
# =>
# ('18679',
#  {'Album': 'Voyagers',
#   'Artist': 'Ben Bova',
#   'Bit Rate': 128,
#   'Compilation': True,
#   'Date Added': datetime.datetime(2011, 7, 23, 1, 46, 42),
#   'Date Modified': datetime.datetime(2012, 2, 20, 3, 24, 40),
#   'Disc Count': 12,
#   'Disc Number': 7,
#   'Equalizer': 'Spoken Word',
#   'File Folder Count': 4,
#   'File Type': 1297106739,
#   'Genre': 'Books & Spoken',
#   'Grouping': 'voyagers',
#   'Kind': 'MPEG audio file',
#   'Library Folder Count': 1,
#   'Location': 'file:///Volumes/External%20Data/Shared/music/Audiobooks/Ben%20Bova/7-11%207k.mp3',
#   'Name': '7k',
#   'Normalization': 947,
#   'Part Of Gapless Album': True,
#   'Persistent ID': 'E11F69D52E536745',
#   'Sample Rate': 44100,
#   'Size': 3162808,
#   'Total Time': 197537,
#   'Track Count': 21,
#   'Track ID': 18679,
#   'Track Number': 11,
#   'Track Type': 'File',
#   'Year': 2006})


