meetup-spreader-python
======================

run.py when run will tweet any meetups happening today that it has not already
tweeted.

before running run.py you need to source setup.sh, this will set up a
virtualenv and install the required packages as well as setting up the
environment variables needed for interfacing with meetup and twitter (by
sourcing secrets.sh)

before sourcing setup.sh you need to edit it and change the paths at the top of
the file.

To run with cron, clone this repository and:
* change the setup.sh to reflect the environment
* make /var/log/meetupTwitterer.py writable by the script
* add an entry to crontab

#### Entry in crontab
I created a script for cron to run so that the environment variables would be
set correctly. You may know a better way. My script looked like this:
```
  1 #!/usr/bin/env bash
  2 source /home/fran/random/meetup-spreader-python/setup.sh
  3 python /home/fran/random/meetup-spreader-python/run.py
```

and my entry in crontab looks like:
```
04 04 * * * /home/fran/random/meetup-spreader-python/run.sh > /tmp/francron.log 2>&1
```

### How the script works
Basic flow of control is:
* the twitter event store processes new events
* the twitter event store reports the events for today that have not already been
tweeted
* the twitterer tweets the events
* the twitter event store marks those events as tweeted
