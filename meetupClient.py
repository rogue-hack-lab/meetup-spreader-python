""" Get rogue hack lab meetup events using the meetup api. """

from datetime import datetime
import logging
import os
import urllib

import requests

MEETUP_GROUP_URLNAME = "Rogue-Hack-Lab"

class MeetupClient(object):
    def __init__(self):
        self.urlRoot = 'https://api.meetup.com/2/events?'
        self.params = {
            'group_urlname': MEETUP_GROUP_URLNAME,
            'key': os.environ.get('MEETUP_API_KEY'),
            }

    def genUrl(self):
        return '%s%s' % (self.urlRoot, urllib.urlencode(self.params))

    def getEventsJson(self):
        #import pickle
        #return pickle.load(open('/tmp/fran.pck'))
        return requests.get(self.genUrl()).json()

class Event(object):
    @classmethod
    def fromJson(cls, jsonData):
        """
        Example json:

        {u'announced': True,
         u'created': 1371586479000,
         u'description': u'<p>The folks at the Ashland Art Center (<a href="http://www.ashlandartcenter.org/" class="linkified">http://www.ashlandartcenter.org/</a>) have invited us to come and have a table display about the Hack Lab on Friday, July 5th. Emile is coordinating (contact at emile.snyder@gmail.com to help out, ask questions, etc.) Plan is to go set up some of the projects that members have worked on and hang out to talk about the Hack Lab, hand out flyers, etc..</p>',
         u'duration': 10800000,
         u'event_url': u'http://www.meetup.com/Rogue-Hack-Lab/events/125282002/',
         u'group': {u'group_lat': 42.310001373291016,
                    u'group_lon': -122.87999725341797,
                    u'id': 4767212,
                    u'join_mode': u'open',
                    u'name': u'Rogue Hack Lab',
                    u'urlname': u'Rogue-Hack-Lab',
                    u'who': u'Hackers/Creators'},
         u'headcount': 0,
         u'id': u'125282002',
         u'maybe_rsvp_count': 0,
         u'name': u'First Friday Art Walk, Ashland Art Center',
         u'status': u'upcoming',
         u'time': 1373068800000,
         u'updated': 1371586554000,
         u'utc_offset': -25200000,
         u'venue': {u'address_1': u'357 E. Main St',
                    u'city': u'Ashland',
                    u'country': u'us',
                    u'id': 14086502,
                    u'lat': 42.195068,
                    u'lon': -122.710426,
                    u'name': u'Ashland Art Center',
                    u'repinned': False,
                    u'state': u'OR',
                    u'zip': u'97520'},
         u'visibility': u'public',
         u'waitlist_count': 0,
         u'yes_rsvp_count': 4}
        """
        ev = cls()
        ev.data = jsonData
        return ev

    def parseTime(self, timeStr):
        return datetime.fromtimestamp(float(timeStr)/1000.0)

    def __getattr__(self, attrName):
        val = self.data[attrName]
        timeFieldNames = ['created', 'time', 'updated']
        if attrName in timeFieldNames:
            val = self.parseTime(val)
        return val

def getEvents():
    """ Convenience function for users of this module to get events. """
    eventsJson = MeetupClient().getEventsJson()
    logging.debug('meetup response keys: %s' % eventsJson.keys())
    if 'problem' in eventsJson:
        message = 'There was a problem getting info from meetup: %s' % eventsJson['problem']
        logging.debug(message)
        raise RuntimeError(message)
    return [Event.fromJson(jev) for jev in
            eventsJson['results']]

if __name__ == '__main__':
    for ev in getEvents():
        print ev.name, ev.time
