#!/usr/bin/env python3.6
# vim: ts=4 sw=4

import configparser, sys
import feedparser, lxml.html, unicodedata, re, os
import twitter
from html import unescape

## String counter for Twitter
def get_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWAH':
            count += 2
        else:
            count += 1
    return count

## String getter for Twitter
def get_truncated_str(text, str_max=280):
    body  = ''
    count = 0
    for c in text:
        count += get_width_count(c)
        if count > str_max: break
        body  += c
    return body

## String truncater for Twitter
def get_twitter_text(text, link):
    if get_width_count(text) <= 252:
        return text + ' ' + link
    else:
        return get_truncated_str(text,248) + '…… ' + link


## Checking config file
arg = sys.argv
if len(arg) >= 2:
    conf_file = arg[1]
else:
    conf_file = os.path.dirname(os.path.abspath(__file__)) + '/' + 'mastodon2twitter.ini'

if not os.path.isfile(conf_file):
    print('config file ' + conf_file + ' is not found')
    sys.exit()

## Initializing
inifile  = configparser.ConfigParser()
inifile.read(conf_file, 'UTF-8')
url      = inifile.get('mastodon', 'url')
tmpfile  = '/tmp/' + os.path.basename(conf_file) + '_lastarticle.dat'
articles = []
posts    = []

## tmpfile check
if os.path.isfile(tmpfile):
    f = open(tmpfile, 'r')
    last_article = f.readline()
    f.close()
else:
    last_article = '0'

## Getting articles from Mastodon
rss = feedparser.parse(url)

for article in rss['entries']:
    htmlstr = article['summary'].replace('<br />', '\n').replace('</p><p>', '\n\n')
    content = re.sub('<[^>]*?>', '', htmlstr)
    if content is None: continue
    
    link    = article['link']
    cont_id = re.sub('^.*/', '', link)
    articles.append(dict(cont_id=cont_id, content=content, link=link))

## Posting articles to TWitter
for article in articles:
    if article['cont_id'] <= last_article: break
    posts.append(get_twitter_text(unescape(article['content']), article['link']))
    # print(get_twitter_text(unescape(article['content']), article['link']))

for post in reversed(posts):
    auth = twitter.OAuth(consumer_key=inifile.get('twitter', 'key'),
                         consumer_secret=inifile.get('twitter', 'sec'),
                         token=inifile.get('twitter', 'tokenkey'),
                         token_secret=inifile.get('twitter', 'tokensec'))
    t = twitter.Twitter(auth=auth)
    t.statuses.update(status=post)
    # print(post)

## Save last article number to tmpfile
try:
    if articles[0]['cont_id'] != last_article:
        f = open(tmpfile, 'w')
        f.write(articles[0]['cont_id'])
        f.close()
except IndexError:
    pass

