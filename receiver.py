from daemon import Daemon
from mq import MQ
import sys
import json
from db import DB
import threading


class Receiver(Daemon):

    stream = None

    def __init__(self, pid_file):
        """
        Constructor
        """
        Daemon.__init__(self, pid_file)

    def setup(self):
        self.setup_db()
        self.delete_old()
        self.setup_mq()

    def setup_db(self):
        db = DB()
        self.conn = db.get_conn()

    def setup_mq(self):
        self.mq = MQ()
        self.mq.init_consumer(self.callback)
        self.mq.consumer.start_consuming()

    def run(self):
        self.setup()

    def callback(self, ch, method, properties, body):
        self.insert_tweet(body)

    def delete_old(self):
        threading.Timer(300.0, self.delete_old).start()  # called every minute
        cur = self.conn.cursor()
        cur.execute("DELETE FROM twitter.tweet WHERE recorded_at <= now() - (10 * interval '1 minute')")
        self.conn.commit()

        cur.execute("DELETE FROM twitter.tweet_hashtag WHERE tweet_id NOT IN (SELECT id FROM twitter.tweet)")
        self.conn.commit()

        cur.close()


    def insert_tweet(self, body):
        tweet = json.loads(body.decode('utf-8'))
        cur = self.conn.cursor()
        hashtags = tweet['hashtags']
        cur.execute(
            'INSERT INTO twitter.tweet (id, user_id, user_name, tweet_text, retweeted, retweet_count, favorite_count, search_key) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (tweet['id'], tweet['user_id'], tweet['user'], tweet['text'], tweet['retweeted'], tweet['retweet_count'], tweet['favorite_count'], tweet['search_key']))
        self.conn.commit()

        for tag in hashtags:
            cur.execute(
                'INSERT INTO twitter.tweet_hashtag (tweet_id, hashtag) '
                'VALUES (%s, %s)',
                (tweet['id'], tag['text']))
            self.conn.commit()
        cur.close()

if __name__ == "__main__":
    daemon = Receiver('/tmp/tweets-receiver.pid')
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


