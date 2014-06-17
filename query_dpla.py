#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# By Tim Walsh, for QueryDPLA

# Searches the Digital Public Library of America (DPLA) for a term tweeted 
# at it and responds with the title and URL of a random item from the 
# query's results.

from dpla.api import DPLA
import random
import tweepy

consumer_key = 'xxxxx'
consumer_secret = 'xxxxx'
access_key = 'xxxxx'
access_secret = 'xxxxx'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        
        # get data from tweet
        
        querier = status.author.screen_name
        twt = status.text
        twt_term = twt.replace("@QueryDPLA ", "")
            
        # search DPLA

        dpla = DPLA('xxxxx') # your DPLA API key here
        result = dpla.search(q="%s" % twt_term, fields=["sourceResource.title", "id"])
            
        # pick random result, fetch and prepare DPLA metadata
    
        json_data = result.items[random.randint(0,5)]
        title = json_data['sourceResource.title']
        title = title[:100]
        json_id = json_data['id']
        item_url = 'http://dp.la/item/%s' % json_id
        
        # tweet DPLA metadata at querier
            
        api.update_status(".%s %s %s" % (querier, title, item_url), 
        in_reply_to_status_id = status.id)
            
    def on_error(self, status_code):
        return True

    def on_timeout(self):
        return True

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['@QueryDPLA'])
