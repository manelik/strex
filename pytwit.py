#!/usr/bin/python

import twitter
import sys



# a file named passes containing two lines of text must exist
# is used to store username and pass
passes = open('passes','r')
user = passes.readline()
passs = passes.readline()
user=user.replace('\n','')
passs=passs.replace('\n','')

passes.close()

loggin=['-li','-lo']
flags=['-ft','-ut','-u']

if loggin.count(sys.argv[1]) :
    if sys.argv[1]=='-li' :
        user = sys.argv[sys.argv.index('-li')+1]
        passs = sys.argv[sys.argv.index('-li')+2]
        passes = open('passes','w')
        passes.write(user+'\n') 
        passes.write(passs+'\n') 
        passes.close()

    elif sys.argv[1]=='-lo' :
        passes = open('passes','w')
        passes.write('\n') 
        passes.write('\n') 
        passes.close()

elif flags.count(sys.argv[1]) :
    api=twitter.Api(username=user,password=passs)

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
        api.PostUpdate(message.strip())
else :
    print 'Unrecognized flag'
