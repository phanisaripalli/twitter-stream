from stream_listener import StreamListener
import tweepy
from daemon import Daemon
from mq import MQ
import sys
import os
import config

class TwitterStream(Daemon):

    stream = None

    def __init__(self, pid_file):
        """
        Constructor
        """
        Daemon.__init__(self, pid_file)
        self.search_key = 'harvey'

    def setup(self):
        """
        Setup DB connections, message queue producer and the Twitter stream
        listener.
        """
        self.set_stream_listener()
        self.setup_mq()
        self.start_listener()

    def setup_mq(self):
        self.mq = MQ()
        self.mq.init_producer()

    def start_listener(self):
        self.stream_listener.filter(track=['harvey'], languages=['en'])

    def run(self):
        self.setup()

    def set_stream_listener(self):
        consumer_key = config.consumer_key
        consumer_secret = config.consumer_secret
        access_key = config.access_key
        access_secret = config.access_secret

        if not TwitterStream.stream:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)
            stream_listener = StreamListener()
            stream_listener.set_stream(self)
            self.stream_listener = tweepy.Stream(auth=auth, listener=stream_listener)
        else:
            print(2)

if __name__ == "__main__":
    daemon = TwitterStream('/tmp/tweets-sender.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)


