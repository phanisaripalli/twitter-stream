import tweepy
import time
import json

class StreamListener(tweepy.StreamListener):


    def on_status(self, status):
        message = {'id': status.id,
                   'text': status.text,
                   'user': status.user.screen_name,
                   'user_id': status.user.id,
                   'retweeted': status.retweeted,
                   'coordinates': status.coordinates,
                   'retweet_count': status.retweet_count,
                   'favorite_count': status.favorite_count,
                   'retweeted': status.retweeted,
                   'hashtags': status.entities['hashtags'],
                   'time': int(time.time()),
                   'search_key': self.stream.search_key}
        self.stream.mq.producer.publish(json.dumps(message))


    def get_stream(self, auth, stream_listener):
        return tweepy.Stream(auth=auth, listener=stream_listener)

    def on_error(self, status_code):
        print('An error has occurred! Status = %s' % status_code)
        return True  # Don't kill the stream

    def set_stream(self, t):
        """
        Set Stream class object - for producer etc.
        """
        self.stream = t