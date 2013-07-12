
from datetime import datetime
import logging

import twitterer
import twitterEventStore
from wiki import generateTemplateTextFile

def tweetTodaysEvents():
    twit = twitterer.Twitterer()
    store = twitterEventStore.Store()
    store.processNewEvents()
    date = datetime.today()
    for ev in store.getEventsOnDay(date):
        logging.info('tweeting event: %s' % ev)
        twit.tweetEvent(ev)
        store.eventTweeted(ev)
    generateTemplateTextFile.main()


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/meetupTwitterer.log',
            level=logging.DEBUG,
            format='%(asctime)s %(message)s')
    logging.info('starting ******************************************')
    tweetTodaysEvents()
    logging.info('done')

