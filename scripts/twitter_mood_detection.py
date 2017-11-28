#Import Tweepy, a Twitter API wrapper
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import time
import os
import sys
import string
import json
import requests
import serial
import serial.tools.list_ports

#All printable characters
printables = set(string.printable)

#Twitter API information
ckey = '5dQSN5EqZYQTkbrFy75wmzteV'
csecret = 'z3w5OlGbwhh5gnKHrvVTv4tenoHJXyWRnFSWzvXnHLN9PnPjiV'
atoken = '710248910950895616-bDm3kPxAGMRJ11qBGkwT55Gkd22iozM'
asecret = 'xJiyTj8oMBUQEtoEjR6Qm8qhiNW5XLOaWt1yASn8F2I0d'

#Watson API information
features = {"emotion": {}}
version = '2017-02-27'
base_url = 'https://gateway.watsonplatform.net'
params = {'version': '2017-02-27'}
em_username = '6c7f54db-a128-4248-8969-ce10eeede157'
em_password = 'OHQMSbdEC2wj'
em_url = '/natural-language-understanding/api/v1/analyze'
em_headers = {'content-type': 'application/json', 'accept': 'application/json', 'user-agent': 'watson-developer-cloud-python-0.26.1'}
id_username = 'f6beacdd-c132-4add-ae11-aa35f3e4304a'
id_password = 'APNcey2h7hYG'
id_url = '/language-translator/api/v2/identify'
id_headers = {'content-type': 'text/plain', 'accept': 'application/json', 'user-agent': 'watson-developer-cloud-python-0.26.1'}

#Setup arduino port
ports = list(serial.tools.list_ports.comports())
port = ports[0][0]
arduino = serial.Serial(port, 9600)
arduino.flush()

#Listen to stream of tweets
class Listener(StreamListener):
    def __init__(self):
        self.tweets = [[]]

    #When data is received
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = self.get_tweet(data)
            if self.is_english(tweet):
                self.tweets[-1].append(tweet)

            #When 10 tweets have been received
            if len(self.tweets[-1]) >= 10:
                emotions = self.get_emotional_content()["emotion"]["document"]["emotion"]

                #Scale emotional values
                emotions["anger"] += 0.1867141506/2
                emotions["disgust"] += 0.1158268397/2
                emotions["fear"] += 0.3500829744/2
                emotions["joy"] += 0
                emotions["sadness"] += 0.1070324615/2
                sorted_emotions = self.sort_dict_by_values(emotions)
                print(sorted_emotions)
                print()
                print("\n<><><><>\n".join(self.tweets[-2]))
                print()
                arduino.write((sorted_emotions[0][0][:1]+str(sorted_emotions[0][1])).encode())                    
                return False
        except BaseException as e:
            print("Error in on_data({0}): {1}".format(e.errno, e.strerror))
            time.sleep(15)
        return True

    #When Twitter API returns error code
    def on_error(self, status):
        print("Received error code {0} from Twitter API".format(status))
        return True

    #Converts dictionary to list of tuples, ordered by value
    def sort_dict_by_values(self, dictionary):
        return sorted(zip(list(dictionary.keys()), list(dictionary.values())), key=lambda x: x[1], reverse=True)

    #Gets emotional content from IBM Watson
    def get_emotional_content(self):
        data = {"clean": True, "features": features, "fallback_to_raw": True, "return_analyzed_text": False, "text":"\n".join(self.tweets[-1])}
        self.tweets.append([])
        response = requests.request(method="POST", url=base_url + em_url, auth=(em_username, em_password), headers=em_headers, params=params, data=json.dumps(data)).json()
        return response

    #Identifies the language of a tweet using Watson
    def get_language(self, tweet):
        data = {"text": tweet}
        response = requests.request(method="POST", url=base_url + id_url, auth=(id_username, id_password), headers=id_headers, params=params, data=json.dumps(data)).json()
        return response["languages"]

    #Determines if a tweet is in English
    def is_english(self, tweet):
        if len(list(filter(lambda x: x in printables, tweet)))/len(tweet) < 0.75:
            return False
        langs = self.get_language(tweet)
        for lang in langs:
            if lang["language"] == 'en' and lang['confidence'] > 1/2:
                return True
        return False

    #If a tweet is a retweet, the RT portion at the start may cause the text of the tweet to be longer than the character limit, and will subsequently be cut off by Twitter.
    #In order to get the full text, you have to check if it is a retweet first, then get the full text from the appropriate key.
    def get_tweet(self, data):
        if "retweeted_status" in list(data.keys()):
            if "extended_tweet" in list(data["retweeted_status"].keys()):
                return data["retweeted_status"]["extended_tweet"]["full_text"]
            else:
                return data["retweeted_status"]["text"]
        elif "text" in list(data.keys()):
            return data["text"]
        else:
            raise Exception(strerror="Could not get text from tweet")
            return None


if __name__ == '__main__':

    #Instantiate and authenticate Twitter API 
    args = "Namespace(query=\'"
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    for i in range(10):

        #Get trending hashtags
        trends1 = api.trends_place(1)
        hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]
        if (os.path.exists("hashtags/trending_hashtags.txt")):
            os.remove("hashtags/trending_hashtags.txt")
        outfile = "hashtags/trending_hashtags.txt"
        with open(outfile, 'a') as f:
            for hashtag in hashtags:
                try:
                    # necessary write command - automatically filters out incompatible hashtags
                    f.write(hashtag + "\n")
                    # print(hashtag)
                    args += hashtag + ","
                except BaseException as e:
                    print("Invalid Hashtag (foreign language, unsupported characters, etc): " + hashtag)
                    pass

        args = args[:-1]
        args += "\')"

        #Open Twitter stream
        twitter_stream = Stream(auth, Listener())
        twitter_stream.filter(track=[args], async=True)
        time.sleep(30)

    arduino.close()