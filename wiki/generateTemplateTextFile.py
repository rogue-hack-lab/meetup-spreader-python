import os
from datetime import datetime
from datetime import timedelta

from twitterEventStore import Store

pageTemplate = """==== Hack Lab Events ====
From '''%(startDate)s''' - '''%(endDate)s'''"""

entryTemplate = """* [%(url)s %(label)s]"""

def makeLabelForEvent(event):
    def timeFormat(time):
        s = time.strftime('%I:%M %p')
        if s.startswith('0'):
            s = s[1:]
        return s
    dateFormat = '%A'
    timeStr = '%s %s' % (event.time.strftime(dateFormat), timeFormat(event.time))
    return '%s ::: %s ::: %s' % (event.name, event.venue['name'], timeStr)

def getEvents(startDay, endDay):
    return Store().getEventsBetweenDaysInclusive(startDay, endDay)

def main():
    today = datetime.today()
    startDate = today
    endDate = today + timedelta(days=6)
    timeFormat = '%A %B %d'
    strStartDate = startDate.strftime(timeFormat)
    strEndDate = endDate.strftime(timeFormat)
    s = pageTemplate % {'startDate': strStartDate, 'endDate': strEndDate}
    for ev in getEvents(startDate, endDate):
        line = entryTemplate % {'url': ev.event_url, 'label':
                makeLabelForEvent(ev)}
        s += '\n%s' % line
    path = os.path.join(os.path.dirname(__file__), 'meetupWikiTemplateContents.txt')
    open(path, 'w').write(s)

