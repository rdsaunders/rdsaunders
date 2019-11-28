from datetime import datetime
import json
import os
import posixpath
import sys
import re

# Path to store tweets
tweet_path = "_tweets"

# -------------------------------------------
# Tweet filenames based on original tweet ID
# -------------------------------------------
tweet_file_template = "{tweet_id}.md"

# -------------------------------------------
# Markdown template
# -------------------------------------------
tweet_yml_template = """---
title: "{tweet_id}"
date: {date}
original-tweet-id: "{tweet_id}"
retweets: {retweet_count}
favorites: {favorite_count}
reply-tweet-id: "{reply_tweet_id}"
reply-user-id: "{reply_user_id}"
reply-user-screen-name: "{reply_user_screen_name}"
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

# -------------------------------------------
# Load JSON
# -------------------------------------------
with open(twitter_export_file) as fd:
    data = json.load(fd)

for tweet in data:

    # -------------------------------------------
    # Create variables of the tweet data
    # -------------------------------------------

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

    # --------------------------------------------------
    # @todo: Convert twitter shortened URLs to originals
    # --------------------------------------------------


    # -------------------------------------------
    # Look for any URLs and convert to HTML links
    # -------------------------------------------
    _link = re.compile(r'(?:(https://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)

    def convertLinks(text): 
        def replace(match):
            groups = match.groups()
            protocol = groups[0] or ''  # may be None
            www_lead = groups[1] or ''  # may be None
            return '<a href="https://{1}{2}">{0}{1}{2}</a>{3}{4}'.format(
                protocol, www_lead, *groups[2:])
        return _link.sub(replace, text)

    full_text_linked = convertLinks(full_text)

    # ----------------------------------------------------------
    # Look for any @mentions and convert to twitter profile links
    # ----------------------------------------------------------

    _mention = re.compile(r'@([^:\s]+)', re.I)

    def convertMentions(text): 
        def replace(match):
            groups = match.groups()
            return '<a href="https://twitter.com/{0}">@{0}</a>'.format(*groups[0:])
        return _mention.sub(replace, text)

    full_text_mention_links = convertMentions(full_text_linked)

    # -------------------------------------------
    # Setup the YAML Template
    # -------------------------------------------
    post = tweet_yml_template.format (
        tweet = full_text_mention_links,
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

    # -------------------------------------------
    # Write files to path specified in post_path
    # -------------------------------------------
    
    post_path = os.path.join(tweet_path, tweet_file)

    try:
        os.makedirs(os.path.dirname(post_path))
    except OSError as err:
        # Ignore "directory exists" errors
        if err.errno != 17:
            raise

    with open(post_path, 'w') as fd:
        fd.write(post)