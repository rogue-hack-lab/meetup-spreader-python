""" tweet events. """
import os
import logging

import tweepy

class Twitterer(object):
    def composeTweet(self, event):
        def timeFormat(time):
            s = time.strftime('%I:%M %p')
            if s.startswith('0'):
                s = s[1:]
            return s
        return 'Today: %s %s %s' % (
                event.name,
                timeFormat(event.time),
                event.venue['name']
                )

    def tweetEvent(self, event):
        self.tweet(self.composeTweet(event))

    def tweet(self, text):
        logging.info('attempting to tweet: %s' % text)
        auth = tweepy.OAuthHandler(
                os.environ['TWITTER_CONSUMER_KEY'],
                os.environ['TWITTER_CONSUMER_SECRET']
                )
        auth.set_access_token(
                os.environ['TWITTER_ACCESS_TOKEN'],
                os.environ['TWITTER_ACCESS_TOKEN_SECRET']
                )
        api = tweepy.API(auth)
        api.update_status(text)

if __name__ == '__main__':
    Twitterer().tweet('still testing ... ')

