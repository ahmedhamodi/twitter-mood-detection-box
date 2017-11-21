#Import Tweepy, a Twitter API wrapper
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import time
import os
import sys
import argparse
import string
import json
import requests

import serial
import serial.tools.list_ports


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
em_username = '7caf2a5f-b43f-4179-bcaf-48c639026d99'
em_password = 'x715aBvw1aYC'
em_url = '/natural-language-understanding/api/v1/analyze'
em_headers = {'content-type': 'application/json', 'accept': 'application/json', 'user-agent': 'watson-developer-cloud-python-0.26.1'}
id_username = '526124a9-0918-44f0-9eba-4562e85d0e10'
id_password = 'zHiVLqvEC3kw'
id_url = '/language-translator/api/v2/identify'
id_headers = {'content-type': 'text/plain', 'accept': 'application/json', 'user-agent': 'watson-developer-cloud-python-0.26.1'}

#Setup arduino port
ports = list(serial.tools.list_ports.comports())
port = ports[0][0]
arduino = serial.Serial(port, 9600)
arduino.flush()



# #Parse command line arguments
# def get_parser():
#     parser = argparse.ArgumentParser(description="Tweet Downloader")
#     parser.add_argument("-q",
#                         "--query",
#                         dest="query",
#                         help="Query/Filter",
#                         default='-')
#     return parser

#Listen to stream of tweets
class Listener(StreamListener):
    def __init__(self):
        # query_fname = format_filename(query)
        # self.outfile = "data/output.txt"
        self.tweets = [[]]

    def on_data(self, data):
        try:
            # f.write(data2 + "\n\n")
            data = json.loads(data)
            # print(data['text'])
            # print(data['retweeted_status'])
            # print(data['retweeted_status']['text'])
            # print(data['retweeted_status']['extended_tweet'])
            # print(data['retweeted_status']['extended_tweet']['full_text'])
            # return False
            tweet = self.get_tweet(data)
            # print(self.get_language(tweet)[:5])
            # print(self.is_english(tweet))
            # print()
            if self.is_english(tweet):
                # print(tweet)
                self.tweets[-1].append(tweet)
            # print(self.tweets[-1])
            if len(self.tweets[-1]) > 10:
                emotions = self.get_emotional_content()["emotion"]["document"]["emotion"]
                sorted_emotions = self.sort_dict_by_values(emotions)
                print(sorted_emotions)
                print()
                arduino.write((sorted_emotions[0][0][:1]+str(sorted_emotions[0][1])).encode())
                if max(list(emotions.values())) > 0.0:
                    print("\n<><><><>\n".join(self.tweets[-2]))
                # print(self.get_emotional_content())
                return False
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            # print(self.tweets[-1])
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True

    def sort_dict_by_values(self, dictionary):
        return sorted(zip(list(dictionary.keys()), list(dictionary.values())), key=lambda x: x[1], reverse=True)

    #Gets emotional content from IBM Watson
    def get_emotional_content(self):
        # print(self.tweets[-1])
        data = {"clean": True, "features": features, "fallback_to_raw": True, "return_analyzed_text": False, "text":"\n".join(self.tweets[-1])}
        # print(data["text"])
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
        # print("text", "text" in list(data.keys()))
        # print("retweeted_status", "retweeted_status" in list(data.keys()))
        if "retweeted_status" in list(data.keys()):
            if "extended_tweet" in list(data["retweeted_status"].keys()):
                return data["retweeted_status"]["extended_tweet"]["full_text"]
            else:
                return data["retweeted_status"]["text"]
        elif "text" in list(data.keys()):
            return data["text"]
        else:
            # print(data)
            return "null"

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    # parser = get_parser()
    # args = parser.parse_args()
    args = "Namespace(query=\'"
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    for i in range(60):
        trends1 = api.trends_place(1)
        # print (trends1)
        hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]

        # stores hashtags in subdirectory
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
                    # print("Invalid Hashtag (foreign language, unsupported characters, etc): %s" % str(e))
                    pass

        args = args[:-1]
        args += "\')"
        # print(args)
        twitter_stream = Stream(auth, Listener())
        twitter_stream.filter(track=[args], async=True)
        time.sleep(60)
        # twitter_stream = Stream(auth, Listener("Trump"), tweet_mode='extended')
        # twitter_stream.filter(track=["Trump"], async=True)
        # filter based on hashtags from a text file
    arduino.close()