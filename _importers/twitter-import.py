import codecs
from datetime import datetime
import json
import os
import posixpath
import re
import shutil
import sys

# This script will import your instagram photos to your static site. It should work for most, assuming you customize the POST_TEMPLATE to match what your site uses.
# Things to note:
#   * multi-photo posts will be imported as standalone photos with no caption (that's how Instagram exports them)
#   * hashtags get removed from posts, unless you set REMOVE_HASH_TAGS to False.
#   * multiline instagram posts are not handled gracefully if you're using the default POST_TEMPLATE (instagram image caption doesn't work with new lines)

# Configuration parameters START

# All of these paths will be strftime formatted with capture time
#BLOG_PATH = "content/blog/%Y/%m"
BLOG_PATH = "_tweets"
#MEDIA_PATH = "content/media/images/photos/%Y/%m"
MEDIA_PATH = "assets/uploads/%Y/%m"
#MEDIA_URL = "/media/images/photos/%Y/%m"
MEDIA_URL = "assets/uploads/%Y/%m"

# BLOG_POST_FILE_TEMPLATE will be formatted with parameters: capture_time, stub
BLOG_POST_FILE_TEMPLATE = "{capture_time:%Y}-{capture_time:%m}-{capture_time:%d}-{slug:s}.md"

# POST_TEMPLATE will be formatted with post_time, caption, and photo_file parameters. Photo file is full path derived from MEDIA_URL
#POST_TEMPLATE = """---
#type: photo
#created: !!timestamp '{post_time:%Y-%m-%d %H:%M:%S}'
#tags:
#    - microblog
#---
#![{caption:s}]({photo_path:s})
#
#"""

POST_TEMPLATE = """---
title: "{caption:s}"
caption: "{caption:s}"
date: {post_time:%Y-%m-%d %H:%M}
location: "{location}"
tags: "{tags:s}"
image: {photo_path:s}
---
"""

REMOVE_HASH_TAGS = True

# Configuration parameters END

if len(sys.argv) < 2:
    print 'First parameter has to be path to directory with Instagram data'
    exit(1)

instagram_data = sys.argv[1]
media_file = os.path.join(instagram_data, 'media.json')
data = {}

if not os.path.exists(instagram_data) or not os.path.exists(media_file):
    print """Directory "{:s}" doesn't exist or is missing media.json file"""
    exit(1)

with open(media_file) as fd:
    data = json.load(fd)

photos = data.get('photos', [])

for photo in photos:

    if REMOVE_HASH_TAGS:
        caption = re.sub(r'#[^\n\s]+', '', photo['caption']).strip()

    # Encode everything as UTF-8
    caption = codecs.encode(caption, 'utf-8')
    capture_time = datetime.strptime(photo['taken_at'], "%Y-%m-%dT%H:%M:%S")
    instagram_photo_path = os.path.join(instagram_data, photo['path'])
    location = codecs.encode(photo.get('location', ''),'utf-8')
    tags = re.findall(r'#[^\n\s]+', photo['caption'])
    taglist = [tag.encode('utf-8') for tag in tags]
    cleantaglist = map(lambda each:each.strip("#"), taglist)
    flatlist = ' '.join(map(str, cleantaglist)) 

    # If the image file is not there, move on. If you don't want to import certain images, just delete them first.
    if not os.path.exists(instagram_photo_path):
        continue

    blog_path = datetime.strftime(capture_time, BLOG_PATH)
    media_path = datetime.strftime(capture_time, MEDIA_PATH)
    media_url = datetime.strftime(capture_time, MEDIA_URL)

    photo_file = os.path.basename(instagram_photo_path)

    post = POST_TEMPLATE.format(
        post_time=capture_time,
        caption=caption,
        photo_path=posixpath.join(media_url, photo_file),
        location=location,
        tags= flatlist
    )

    post_file = None

    if caption:
        slug = re.sub(r"[^a-z0-9 ]", '', caption.lower()).strip()
        slug = re.sub(r" (the|a|an) ", ' ', slug).strip()
        slug = re.sub(r"\s+", ' ', slug).strip()
        slug = "-".join(slug.split()[0:3])
        
        post_file = BLOG_POST_FILE_TEMPLATE.format(
            capture_time=capture_time,
            slug=slug
        )

        # If the filename derived from caption exists, don't use it
        if os.path.exists(os.path.join(blog_path, post_file)):
            post_file = None

    if not post_file:
        post_file = BLOG_POST_FILE_TEMPLATE.format(
            capture_time=capture_time,
            slug="instagram-{:s}".format(os.path.splitext(photo_file)[0])
        )
    
    post_path = os.path.join(blog_path, post_file)

    try:
        os.makedirs(media_path)
        os.makedirs(os.path.dirname(post_path))
    except OSError as err:
        # Ignore "directory exists" errors
        if err.errno != 17:
            raise

    with open(post_path, 'w') as fd:
        fd.write(post)
        shutil.copy(instagram_photo_path, media_path)
