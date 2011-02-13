#!/usr/bin/python


import sys

from oauth import oauth
from oauthtwitter import OAuthApi


# Skynet ready
try:
  import skynet
except ImportError:
  print 'Skynet still unavailable'


# a file named login.info containing two lines of text must exist
# is used to store username and pass
#passes = open('login.info','r')
#user = passes.readline()
#passs = passes.readline()
#user=user.replace('\n','')
#passs=passs.replace('\n','')

#passes.close()

# Parser looks for login.info
# par file contains tuples var&value

auth_data=open('login.info','r')

plines= auth_data.readlines()
auth_data.close()

for x in plines:
  if x.find('tuser')+1 :
    user = x.partition('&')[2].strip()
  elif x.find('tpass')+1 :
    passs = x.partition('&')[2].strip()
#  elif x.find('email')+1 :
    #boyzoBot.email = x.partition('&')[2].strip()
  elif x.find('consumerkey')+1 :
    consumer_key = x.partition('&')[2].strip()
  elif x.find('consumersecret')+1 :
    consumer_secret = x.partition('&')[2].strip()
  elif x.find('otoken')+1 :
    atoken = x.partition('&')[2].strip()
  elif x.find('ostoken')+1 :
    stoken = x.partition('&')[2].strip()


loggin=['-li','-lo']
flags=['-ft','-ut','-u']

if loggin.count(sys.argv[1]) :
    if sys.argv[1]=='-li' :
        user = sys.argv[sys.argv.index('-li')+1]
        passs = sys.argv[sys.argv.index('-li')+2]
        passes = open('login.info','w')
        passes.write('tuser&'+user+'\n') 
        passes.write('tpass&'+passs+'\n') 
        passes.close()

    elif sys.argv[1]=='-lo' :
        passes = open('login.info','w')
        passes.write('\n') 
        passes.write('\n') 
        passes.close()

elif flags.count(sys.argv[1]) :
    api=OAuthApi(consumer_key,consumer_secret,atoken,stoken)

    if sys.argv[1]=='-ft' :
        statuses= api.GetFriendsTimeline(count=20)
        for i in range(len(statuses)):
            print statuses[i].user.name +': '+ statuses[i].text

    elif sys.argv[1]=='-ut' :
        statuses= api.GetUserTimeline(user=sys.argv[2], count=20)
        for i in range(len(statuses)):
            print statuses[i].user.name +': '+ statuses[i].text
            
    elif sys.argv[1]=='-u' :
        message=''
        for s in sys.argv[2:]:
            message+=' '+ s
        api.UpdateStatu(message.strip())
else :
    print 'Unrecognized flag'
