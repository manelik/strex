#!/usr/bin/python


__author__='Jose Manuel Torres'
__version__='alpha_0.1'

import sys
import os

import strexmisc

from oauth import oauth
from oauthtwitter import OAuthApi

# Skynet ready
try:
  import skynet
except ImportError:
#  sys.stderr.write('Skynet still unavailable\n')
  pass # For the time being a failed skynet import won't be
       # reported.

# When skynet is ready is going to be like SURPRISE!! BANG BANG!

# No options, no program
# maybe this will trigger iclient
if len(sys.argv)==1 :
  strexmisc.help_message(1)
  quit()


def make_realtime(hour='00:00:00',lpost='0',lclient='0'):
  real_hour= int(hour.split(':')[0])+lclient-lpost
  if real_hour < 6 : real_hour+= 24

  return str(real_hour)+':'+hour.partition(':')[2]


# Valid flags, there are login related flags
# and action related flags
loggin=['-li','-lo','-su','-au']
flags=['-tl','-ut','-us','-xb','-se','--help','-ir','-iu']
#modifying flags
#
# fetch -f -fu -fs -fi
# time  -t
# post  -p -pi
#
# Configs folder default something like $HOME/.strex
# more on cross-compatibility later
c_folder=os.path.join(os.path.expanduser('~'),'.strex')

plines=[]
# Parser looks for login.info consumer.info

# consumer.info contains app keys in format attribute&value
cons_data=open(os.path.join(c_folder,'consumer.info'),'r')

plines.extend(cons_data.readlines())
cons_data.close()

for x in plines:
  if x.find('consumerkey')+1 :
    consumer_key = x.partition('&')[2].strip()
  elif x.find('consumersecret')+1 :
    consumer_secret = x.partition('&')[2].strip()

# login.info contains the user database
# in format user&attribute:value&atribute:value&...
user_data=open(os.path.join(c_folder,'login.info'),'r')
userraw=user_data.readlines()
userlist=[]
user_data.close()
for x in userraw:
  userlist.append(x.partition('&')[0])

# do some login
if loggin.count(sys.argv[1]) :
  # log-in as a registred user
  if sys.argv[1]=='-li' :
    user = sys.argv[sys.argv.index('-li')+1]
    if userlist.count(user) :
      user_file=open(os.path.join(c_folder,'ulog'),'w')
      user_file.write(user+'\n')
      user_file.close()
    else :
      print 'User not registred'

  elif sys.argv[1]=='-lo' :
        #log-out errases current user 
    user_file=open(os.path.join(c_folder,'ulog'),'w')
    user_file.write('\n')
    user_file.close()
    
  elif sys.argv[1]=='-su' :
    print 'Registred users: '
    for x in userlist:
      print x

  elif sys.argv[1]=='-au' :
    if len(sys.argv)==2:
      strexmisc.help_message(1)
      quit()
      
    #Standard Oauth authentication
    twitter = OAuthApi(consumer_key, consumer_secret)
    # Get the temporary credentials for our next few calls
    temp_credentials = twitter.getRequestToken()
    # Open in firefox or user pastes this into their browser to bring back a pin number
    magic_URL=twitter.getAuthorizationURL(temp_credentials)
    print(magic_URL)
    os.system('firefox '+magic_URL)
    # Get the pin # from the user and get our permanent credentials
    oauth_verifier = raw_input('What is the PIN? ')
    access_token = twitter.getAccessToken(temp_credentials, oauth_verifier)

    # Add user to database    
    user_data=open(os.path.join(c_folder,'login.info'),'a')
    user_data.write(sys.argv[2]+'&'+'token:'+access_token['oauth_token']
                    +'&'+'stoken:'+access_token['oauth_token_secret']
                    +'&'+'lstat:'+'0''\n')
    user_data.close()

# Real actions
elif flags.count(sys.argv[1]) :

  # Parse login file    
  curruser = open(os.path.join(c_folder,'ulog'),'r')
  user = curruser.readline().strip()
  curruser.close()

  for x in userraw:
    if x.find(user)+1 :  
      tempstr=x.partition('&')[2].partition('&')
      while tempstr[0]<>'':
        currstr=tempstr[0].partition(':')
        if currstr[0]=='token':
          atoken= currstr[2].strip()
        elif currstr[0]=='stoken':
          stoken= currstr[2].strip()
        elif currstr[0]=='lstat':
          last_id = int(currstr[2].strip())
        tempstr=tempstr[2].partition('&')

  # Start session
  api=OAuthApi(consumer_key,consumer_secret,atoken,stoken)

  num_statuses=0
  statuses=[]
  call_opts={}

  if sys.argv[1]=='-xb' : #just check if there are new messages for xmobar
    statuses=api.GetHomeTimeline({'since_id':last_id})
    if len(statuses):
      print '<fc=red>New twitts</fc>'
    else:
      print 'No news'

  if sys.argv[1]=='-tl' : # Check friend timeline, update last read status
    # Sanity check
    if len(sys.argv)==2: # No args fetches since the last_id
      num_statuses=20
      call_opts.update({'since_id':last_id})
    elif len(sys.argv)==3:          # argument following -tl is number of 
      num_statuses=int(sys.argv[2]) # statuses fetched
    elif len(sys.argv)>3:
      print 'too many arguments'    # unnecessary args

    call_opts.update({'count':num_statuses})
    statuses=api.GetHomeTimeline(call_opts)

    if len(statuses)>0:
      curr_id=statuses[0]['id']
      new_str='*'
      for i in statuses:
        if int(i['id'])<=last_id:
          if new_str=='*':
            print '----------------------------------------------------------'
          new_str=''
          
        print new_str+i.pop('user').pop('screen_name') +': '+ i.pop('text')
    
      user_data=open(os.path.join(c_folder,'login.info'),'w') # Open database append changes
      for x in userraw:
        if x.find(user)==-1: 
          user_data.write(x)
      user_data.write(user+'&'+'token:'+atoken+'&'+'stoken:'+stoken+'&'
                      +'lstat:'+str(curr_id)+'\n')
      user_data.close()
    else:
      print 'No new updates'

  elif sys.argv[1]=='-ut' : # Check statuses for a specific user
    # Sanity Check
    if len(sys.argv)==3: # No args fetches since the last_id
      num_statuses=20
      call_opts.update({'since_id':last_id})
    elif len(sys.argv)==4:          # argument following -tl is number of 
      num_statuses=int(sys.argv[3]) # statuses fetched
    elif len(sys.argv)>4:
      print 'too many arguments'    # unnecessary args

    call_opts.update({'count':num_statuses,'user':sys.argv[2]})
    statuses=api.GetUserTimeline(call_opts)

    for i in statuses:
      print i.pop('user').pop('screen_name') +': '+ i.pop('text')
    
    if len(statuses)==0:
      print 'No new updates from '+sys.argv[2] 

  elif sys.argv[1]=='-us' : # Update status, auto-breaking long ones
    message=''
    for s in sys.argv[2:]:
      message+=' '+ s
    while len(message)>140:
      api.UpdateStatus(message[0:138]+'...')
      message=message[138:]
    api.UpdateStatus(message.strip())

  elif sys.argv[1]=='-se': # Search
    if len(sys.argv)==3:
      num_statuses=20
      call_opts.update({'since_id':last_id})
    elif len(sys.argv)==4:
      num_statuses=int(sys.argv[3])
    elif len(sys.argv)>4:
      print 'too many arguments' 

    call_opts.update({'count':num_statuses,'q':sys.argv[2],
                      'rpp':num_statuses,'result_type':'recent'})
    
    statuses=api.GetSearchResults(call_opts).pop('results')
    for i in statuses:
      print i.pop('from_user')+': '+ i.pop('text')

  elif sys.argv[1]=='-ir': #interactive??

    import time
    local_hour=-6
    loop_flag=True
    if last_id==0:
      call_opts.update({'count':20})
    else :
      call_opts.update({'since_id':last_id})
    while True:
      statuses=api.GetHomeTimeline(call_opts)
      while len(statuses):
        curr_status=statuses.pop(-1)
        last_id=curr_status['id']
        curr_time=curr_status['created_at'].split()[3]
        hour_mod=int(curr_status['created_at'].split()[4])
        curr_time=make_realtime(curr_time,hour_mod,local_hour)
        print (curr_time+' '+curr_status['user']['screen_name']+': '
               + curr_status['text'])
        if (user==curr_status['user']['screen_name'] 
            and curr_status['text'].count('#stop#strex')):
          loop_flag=False
      if not(loop_flag):
        break
      call_opts.update({'since_id':last_id})
      time.sleep(20)

    user_data=open(os.path.join(c_folder,'login.info'),'w') # Open database append changes
    for x in userraw:
      if x.find(user)==-1: 
        user_data.write(x)
    user_data.write(user+'&'+'token:'+atoken+'&'+'stoken:'+stoken+'&'
                    +'lstat:'+str(last_id)+'\n')
    user_data.close()
        
  elif sys.argv[1]=='-iu':
    message=''
    while message<>'q':
      message=raw_input()
      if message<>'q':
        while len(message)>140:
          api.UpdateStatus(message[0:138]+'...')
          message=message[138:]

        api.UpdateStatus(message.strip()).keys()

  elif sys.argv[1]=='--help': # Full help message
    strexmisc.help_message(2)
else :
  strexmisc.help_message(1)


