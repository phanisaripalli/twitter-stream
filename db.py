import psycopg2
import config

class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname=XXX user=XXX password=XXX host=XXXX")
        except:
            print("unable to connect")
            self.conn = None

    def get_conn(self):
        return self.conn
