
# miscelaneous functions module


import urllib2

#import cgi as urlparse  # <= 2.5
import urlparse

import re

def help_message(code):
    ''' Prints the help message.
    Code 
    0   No error. Why call?
    1   Short message
    2   Long message
    '''
    if code==0:
        print 'No error. Why call for help?'
    elif code==1:
        print 'Usage: strex [COMMAND]... [OPTIONS]...'
        print 'Try `strex --help\' for more options.'
    elif code==2:
        print 'STREX alpha, a command line twitter client'
        print 'Usage: strex [COMMAND]... [OPTIONS]...'
        print ''
        print 'Authentication:'
        print '  --login               Log in as a registred user.'
        print '  --logout              Log out.'
        print '  --show                Show registred users.'
        print '  --authenticate USER   Authenticate USER. mandatory.'
        print ''
        print 'Fetch messages:'
        print '  -f  COUNT         Home timeline'
        print '  -u  USER COUNT    USER timeline'
        print '  -s  STRING COUNT  Search for '
        print '  -h                Print the time when it was tweeted'
        print ''
        print 'Post messages:'
        print '  -p  message       Home timeline'
        print '  -u  USER COUNT    USER timeline'
        print
        print 'Misc:'
        print '  -i        idle modes'
        print '  -x        Look for new twitts, xmobar output (not stackeable)'
        print '  --help    This help message'
        print ''
        print 'For bug reports and suggestions contact me at github.com/manelik'
        print ''
#  val_flags= 'fpitusxh'


def parse_urls(messg=''):
    '''Parse the urls contained in a string.
    Returns a list of url matching strings
    '''
    are_urls=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
               , messg )
    return are_urls


def shorten_url(url=''):
    ''' Shorten a url using Tinyurl API.
    recieves url string
    '''
    if url=='':
        return ''
    else :
        opener = urllib2.build_opener()
        url_data = opener.open('http://tinyurl.com/api-create.php?url='+url).read()
        return url_data
    

