import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import json

ckey = '5dQSN5EqZYQTkbrFy75wmzteV'
csecret = 'z3w5OlGbwhh5gnKHrvVTv4tenoHJXyWRnFSWzvXnHLN9PnPjiV'
atoken = '710248910950895616-bDm3kPxAGMRJ11qBGkwT55Gkd22iozM'
asecret = 'xJiyTj8oMBUQEtoEjR6Qm8qhiNW5XLOaWt1yASn8F2I0d'

def get_parser():
    parser = argparse.ArgumentParser(description="Tweet Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser


class listener(StreamListener):
    def __init__(self, query):
        query_fname = format_filename(query)
        self.outfile = "data/output-%s.json" % (query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return ''

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, listener(args.query))
    twitter_stream.filter(track=[args.query])