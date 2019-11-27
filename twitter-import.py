from datetime import datetime
import json
import os
import posixpath
import sys

# Path to store tweets
tweet_path = "_tweets"

# Tweet markdown file template
tweet_file_template = "{tweet_id}.md"

# Markdown template
tweet_yml_template = """---
title: "{tweet_id}"
date: {date}
retweets: {retweet_count}
favorites: {favorite_count}
reply-tweet-id: {reply_tweet_id}
reply-user-id: {reply_user_id}
reply-user-screen-name: {reply_user_screen_name}
---
{tweet}
"""

if len(sys.argv) < 2:
    print ("First parameter has to be path to directory with tweet data")
    exit(1)

tweet_data = sys.argv[1]
twitter_export_file = os.path.join(tweet_data, 'tweet.json')
data = {}

if not os.path.exists(tweet_data) or not os.path.exists(twitter_export_file):
    print ("Directory does not exist or is missing tweet.json file")
    exit(1)

with open(twitter_export_file) as fd:
    data = json.load(fd)

for tweet in data:

    # Tweet
    full_text = tweet['full_text'].encode('utf-8').strip()
    created_at = tweet['created_at']
    id_str = tweet['id_str']
    # Tweet metadata
    favorite_count = tweet['favorite_count']
    retweet_count = tweet['retweet_count']
    # Replies
    reply_tweet_id = tweet.get('in_reply_to_status_id_str', '').encode('utf-8').strip()
    reply_user_id = tweet.get('in_reply_to_user_id_str', '').encode('utf-8').strip()
    reply_user_screen_name = tweet.get('in_reply_to_screen_name', '').encode('utf-8').strip()
    
    #print(reply_user_screen_name)

    post = tweet_yml_template.format (
        tweet = full_text,
        date = created_at,
        tweet_id = id_str,
        favorite_count = favorite_count,
        retweet_count = retweet_count,
        reply_tweet_id = reply_tweet_id,
        reply_user_id = reply_user_id,
        reply_user_screen_name = reply_user_screen_name
    )

    tweet_file = tweet_file_template.format (
        tweet_id = id_str
    )
    
    post_path = os.path.join(tweet_path, tweet_file)

    try:
        os.makedirs(os.path.dirname(post_path))
    except OSError as err:
        # Ignore "directory exists" errors
        if err.errno != 17:
            raise

    with open(post_path, 'w') as fd:
        fd.write(post)