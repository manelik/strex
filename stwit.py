#!/usr/bin/python


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


#passes.close()

# Parser did nothing at this stage!! minimize it!
# Parser looks for login.info consumer.info
# login format user&token&stoken
# 

if len(sys.argv)==1 :
  print 'Here goes help message'
  quit()

plines=[]

cons_data=open('consumer.info','r')

plines.extend(cons_data.readlines())
cons_data.close()



for x in plines:
  if x.find('consumerkey')+1 :
    consumer_key = x.partition('&')[2].strip()
  elif x.find('consumersecret')+1 :
    consumer_secret = x.partition('&')[2].strip()



loggin=['-li','-lo','-su','-au']
flags=['-ft','-ut','-us']

user_data=open('login.info','r')
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
            user_file=open('ulog','w')
            user_file.write(user+'\n')
            user_file.close()
        else :
            print 'User not registred'

    elif sys.argv[1]=='-lo' :
        #log-out 
        user_file=open('ulog','w')
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

        print("oauth_token: " + access_token['oauth_token'])
        print("oauth_token_secret: " + access_token['oauth_token_secret'])
        
        userraw.append(sys.argv[2]+'&'+access_token['oauth_token']+'&'
                       +access_token['oauth_token_secret'])
        user_data=open('login.info','a')
        user_data.write(sys.argv[2]+'&'+access_token['oauth_token']
                        +'&'+access_token['oauth_token_secret']+'\n')
        user_data.close()

elif flags.count(sys.argv[1]) :
    
    curruser = open('ulog','r')
    user = curruser.readline().strip()
    curruser.close()
    for x in userraw:
        if x.find(user)+1 :  
            atoken= x.partition('&')[2].partition('&')[0].strip()
            stoken= x.partition('&')[2].partition('&')[2].strip()
            
    api=OAuthApi(consumer_key,consumer_secret,atoken,stoken)

    if sys.argv[1]=='-ft' :
        statuses= api.GetFriendsTimeline(count=1)
        print statuses
        for i in range(len(statuses)):
            print statuses[i].user.name +': '+ statuses[i].text

    elif sys.argv[1]=='-ut' :
        statuses= api.GetUserTimeline(user=sys.argv[2], count=20)
        for i in range(len(statuses)):
            print statuses[i].user.name +': '+ statuses[i].text
            
    elif sys.argv[1]=='-us' :
        message=''
        for s in sys.argv[2:]:
            message+=' '+ s
        api.UpdateStatus(message.strip())
else :
    print 'Unrecognized flag'
