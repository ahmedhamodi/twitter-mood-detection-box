import tweepy, time, sys, json
from tweepy import OAuthHandler
import os

# argfile = str(sys.argv[0])

#enter the corresponding information from your Twitter application:
ckey = '5dQSN5EqZYQTkbrFy75wmzteV'
csecret = 'z3w5OlGbwhh5gnKHrvVTv4tenoHJXyWRnFSWzvXnHLN9PnPjiV'
atoken = '710248910950895616-bDm3kPxAGMRJ11qBGkwT55Gkd22iozM'
asecret = 'xJiyTj8oMBUQEtoEjR6Qm8qhiNW5XLOaWt1yASn8F2I0d'
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

# filename=open(argfile,'r')
# f=filename.readlines()
# filename.close()

trends1 = api.trends_place(1)
# print (trends1)
hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]

#stores hashtags in subdirectory
if (os.path.exists("hashtags/trending_hashtags.txt")):
    os.remove("hashtags/trending_hashtags.txt")
outfile = "hashtags/trending_hashtags.txt"
with open(outfile, 'a') as f:
    for hashtag in hashtags:
        try:
            f.write(hashtag + "\n")
            print(hashtag)
        except BaseException as e:
            print("Error on_data: %s" % str(e))

# trend_hashtag = hashtags[0]
# api.update_status(line + ' ' + trend_hashtag)