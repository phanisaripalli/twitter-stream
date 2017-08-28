import pika
import logging


class MQ(object):
    def __init__(self):
        self.log = logging.getLogger('mq')
        self.consumer = None
        self.callback = None
        self.producer = None

    def init_consumer(self, callback):
        self.consumer = Consumer(callback)

    def init_producer(self):
        self.producer = Producer()



class Consumer(object):
    def __init__(self, callback):
        """
        Constructor. Initiate connection with RabbitMQ server.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='tweets')
        self.queue = 'tweets'
        self.callback = callback

    def close(self):
        """
        Close channel and connection.
        """
        self.channel.close()
        self.connection.close()

    # this is the callback function we will use to insert the tweets into postgres
    def callback1(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def start_consuming(self):
        self.channel.basic_consume(self.callback,
                                   queue='tweets',
                                   no_ack=True)
        self.channel.start_consuming()


    def wait(self):
        """
        Wait for activity on the channel.
        """
        while True:
            self.channel.wait()


class Producer(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='tweets')

    def publish(self, message):
        """
        Publish message to exchange using routing key
        """
        self.channel.basic_publish(exchange='',
                                   routing_key='tweets',
                                   body=message)

    def close(self):
        """
        Close channel and connection
        """
        self.channel.close()
        self.connection.close()