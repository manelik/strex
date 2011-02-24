

# miscelaneous functions module

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
        print '  -li           Log in as a registred user.'
        print '  -lo           Log out.'
        print '  -su           Show registred users.'
        print '  -au USER      Authenticate USER. mandatory.'
        print ''
        print 'Fetch messages:'
        print '  -tl COUNT         Home timeline'
        print '  -ut USER COUNT    USER timeline'
        print '  -se STRING COUNT  Search for '
        print ''
        print 'Misc:'
        print '  -xb       Look for new twitts, xmobar output'
        print '  --help    This help message'
        print ''
        print 'For bug reports and suggestions contact me at github.com/manelik'
        print ''
