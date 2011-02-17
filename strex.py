#!/usr/bin/python


__author__='Jose Manuel Torres'
__version__='alpha_0.1'

import sys
import os

from oauth import oauth
from oauthtwitter import OAuthApi

# Skynet ready
try:
  import skynet
except ImportError:
#  sys.stderr.write('Skynet still unavailable\n')
  pass



# Parser did nothing at this stage!! minimize it!
# Parser looks for login.info consumer.info
# login format user&attribute:value&atribute:value&...
# 

if len(sys.argv)==1 :
  print 'Here goes help message'
  quit()


#Configs folder

c_folder=os.path.join(os.path.expanduser('~'),'.strex')

plines=[]

cons_data=open(os.path.join(c_folder,'consumer.info'),'r')

plines.extend(cons_data.readlines())
cons_data.close()



for x in plines:
  if x.find('consumerkey')+1 :
    consumer_key = x.partition('&')[2].strip()
  elif x.find('consumersecret')+1 :
    consumer_secret = x.partition('&')[2].strip()



loggin=['-li','-lo','-su','-au']
flags=['-ft','-ut','-us','-xb']

user_data=open(os.path.join(c_folder,'login.info'),'r')
userraw=user_data.readlines()
userlist=[]
user_data.close()
for x in userraw:
  userlist.append(x.partition('&')[0])

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
        #log-out 
    user_file=open(os.path.join(c_folder,'ulog'),'w')
    user_file.write('\n')
    user_file.close()
    
  elif sys.argv[1]=='-su' :
    print 'Registred users: '
    for x in userlist:
      print x

  elif sys.argv[1]=='-au' :
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

  if sys.argv[1]=='-xb' : #just check if there are new messages for xmobar
    statuses=api.GetFriendsTimeline({'count':1})
    curr_id=int(statuses[0].pop('id'))
    if curr_id>last_id :
      print '<fc=red>New twitts</fc>'
    else:
      print 'No news'

  if sys.argv[1]=='-ft' : # Check friend timeline, update last read status
    if len(sys.argv)==2:
      num_statuses=20
    elif len(sys.argv)==3:
      num_statuses=int(sys.argv[2])
    elif len(sys.argv)>3:
      print 'too many arguments' 

    statuses=api.GetHomeTimeline({'count':num_statuses})
    curr_id=statuses[0].pop('id')
    for i in statuses:
      print i.pop('user').pop('screen_name') +': '+ i.pop('text')

    user_data=open(os.path.join(c_folder,'login.info'),'w')
    for x in userraw:
      if x.find(user)==-1:
        user_data.write(x)
    user_data.write(user+'&'+'token:'+atoken+'&'+'stoken:'+stoken+'&'
                    +'lstat:'+str(curr_id)+'\n')
    user_data.close()
    
  elif sys.argv[1]=='-ut' : # Check statuses for a specific user
    if len(sys.argv)==3:
      num_statuses=20
    elif len(sys.argv)==4:
      num_statuses=int(sys.argv[3])
    elif len(sys.argv)>4:
      print 'too many arguments' 

    statuses=api.GetUserTimeline({'user':sys.argv[2], 'count':num_statuses})
    for i in statuses:
      print i.pop('user').pop('screen_name') +': '+ i.pop('text')
            
  elif sys.argv[1]=='-us' : # Update status, auto-breaking long ones
    message=''
    for s in sys.argv[2:]:
      message+=' '+ s
      while len(message)>140:
        api.UpdateStatus(message[0:138]+'...')
        message=message[138:]
      api.UpdateStatus(message.strip())
else :
  print 'Unrecognized flag'


