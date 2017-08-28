﻿CREATE TABLE twitter.tweet(
	id bigint,
    user_id bigint,
    user_name text,
    tweet_text text,
    retweeted boolean,
    retweet_count int,
    favorite_count int,
    recorded_at timestamp default now()
);


alter table twitter.tweet add column search_key text;

CREATE TABLE twitter.tweet_hashtag(
	tweet_id bigint,
    hastag text
);
