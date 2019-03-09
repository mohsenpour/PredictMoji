from tweepy.streaming import StreamListener
from tweepy import  OAuthHandler
from tweepy import Stream
import creds2
import sys





class TwitterStreamer():
    '''
    top level class for processing live tweets
    '''
    def stream_tweets(self, where_to_save_filename, keywords_list):
        # This handles Twitter Authentication and the connection to twitter API
        listener = Listener(where_to_save_filename)
        auth = OAuthHandler(creds2.CONSUMER_KEY, creds2.CONSUMER_SECRET)
        auth.set_access_token(creds2.ACCESS_TOKEN, creds2.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)
        stream.filter(track=keywords_list)

class Listener(StreamListener):
    '''
    listener class to handle lower level data handling functions
    '''
    def __init__(self, where_to_save_filename):
        self.where_to_save_filename = where_to_save_filename
        self.i = 0
    def on_data(self, data):
        try:
            print(data)
            with open(self.where_to_save_filename, 'a') as file:
                file.write(data)
                self.i+=1
            return True
        except BaseException as e:
            print(e)
        return True

    def on_error(self, status):
        if(status == 420):
            print(status)
            return False
if __name__ == '__main__':
    Fear = [u"\U0001F628",u"\U0001F630",,u"\U0001F631"]
    Anger = [u"\U0001F620",u"\U0001F621",u"\U0001F624"]
    Sadness = [u"\U0001F61E",u"\U0001F622",u"\U0001F623",u"\U0001F625",u"\U0001F62D"]
    Joy = [u"\U0001F601",u"\U0001F602",u"\U0001F603",u"\U0001F604"]
    Surprise = [u"\U0001F632",u"\U0001F633",u"\U0001F62E",u"\U0001F62F"]
    keywords= Fear + Anger + Sadness + Joy + Surprise
    where_to_save = 'tweets.txt'
    streamer = TwitterStreamer()
    streamer.stream_tweets(where_to_save, keywords)
