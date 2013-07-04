""" Store events for tweeting. """

import json
import os

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
import sqlalchemy.ext.declarative
import sqlalchemy.orm
from sqlalchemy.sql import extract

import meetupClient

DB_FILE_NAME = 'twitterEventStore.db'

engine = sqlalchemy.create_engine('sqlite:///%s' % DB_FILE_NAME)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
DeclarativeBase = sqlalchemy.ext.declarative.declarative_base()


class Event(DeclarativeBase):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    updated = Column(DateTime, nullable=False)
    time = Column(DateTime, nullable=False)
    jsonData = Column(String, nullable=False)
    tweeted = Column(Boolean, default=False)

    def __repr__(self):
        return '%s, Tweeted=%s' % (self.url, self.tweeted)

    def updateFromMeetupEvent(self, meetupEvent):
        self.url = meetupEvent.event_url
        self.time = meetupEvent.time
        self.updated = meetupEvent.updated
        self.jsonData = json.dumps(meetupEvent.data)

    @classmethod
    def fromMeetupEvent(cls, meetupEvent):
        ev = cls()
        ev.updateFromMeetupEvent(meetupEvent)
        return ev


class Store(object):
    def __init__(self):
        # make the db if it's not there
        if not os.path.exists(os.path.join(__file__, DB_FILE_NAME)):
            DeclarativeBase.metadata.create_all(bind=engine)
        self.session = Session()

    def findEvent(self, meetupEvent):
        res = self.session.query(Event).filter(Event.url==meetupEvent.event_url).all()
        return res[0] if len(res) > 0 else None

    def eventState(self, meetupEvent):
        """
        returns (status, event) where:
          status is one of 'new', 'updated', 'exists'.
          event is a matching event if exists else None
        """
        ev = self.findEvent(meetupEvent)
        if ev is None:
            return 'new', None
        if ev.updated < meetupEvent.updated:
            return 'updated', ev
        return 'exists', ev

    def processEvent(self, event):
        """
        For an event from the meetup api either add, update or ignore it.
        """
        status, existing = self.eventState(event)
        if status == 'new':
            self.session.add(Event.fromMeetupEvent(event))
        elif status == 'updated':
            existing.updateFromMeetupEvent(event)

    # API below
    def getEventsOnDay(self, day):
        """ Return events on the specified day that have not been processed. """
        query = self.session.query(Event
            ).filter(
                extract('year', Event.time) == day.year
            ).filter(
                extract('month', Event.time) == day.month
            ).filter(
                extract('day', Event.time) == day.day
            ).filter(
                Event.tweeted == False
            )
        return [meetupClient.Event.fromJson(json.loads(event.jsonData)) for event in query.all()]

    def processNewEvents(self):
        """ Get the events from meetup and store them. """
        for ev in meetupClient.getEvents():
            self.processEvent(ev)
        self.session.commit()

    def eventTweeted(self, event):
        """ Mark the event tweeted so it won't be tweeted again. """
        self.findEvent(event).tweeted = True
        self.session.commit()


