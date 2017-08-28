# twitter-stream

- Use twitter stream to publish to a RabbitMQ msg queue
- Read from the queue and insert into Postgres DB
- Use Dameons for start and stop service (courtesy: https://github.com/laurentluce/pytolab-trends)
- just in case you have tweepy stream error (attributeerror: 'nonetype' object has no attribute 'strip' tweepy), see https://github.com/tweepy/tweepy/issues/576 as suggested by srwareham 
- Finally show some web based stats/analytics (actual rendering is in https://github.com/phanisaripalli/twitteralli)

![Twitter stats](https://github.com/phanisaripalli/twitter-stream/blob/master/twitter-stats.png)
