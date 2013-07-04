
from datetime import datetime
from datetime import timedelta

import twitterer
import twitterEventStore

def tweetTodaysEvents():
    twit= twitterer.Twitterer()
    store = twitterEventStore.Store()
    store.processNewEvents()
    date = datetime.today()# + timedelta(days=1)
    for ev in store.getEventsOnDay(date):
        twit.tweet(ev)
        store.eventTweeted(ev)

if __name__ == '__main__':
    tweetTodaysEvents()

