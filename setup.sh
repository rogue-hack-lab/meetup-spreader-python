
# Change the following for your env.
WORKING_DIR='/path/to/meetup-spreader-python'
export MEETUP_API_KEY=<key here>
export TWITTER_CONSUMER_KEY=<key here>
export TWITTER_CONSUMER_SECRET=<key here>
export TWITTER_ACCESS_TOKEN=<key here>
export TWITTER_ACCESS_TOKEN_SECRET=<key here>


# This stuff is to set up the application environment.
VIRTUAL_ENV_NAME='meetup-spreader-virtualenv'
PYTHON_LIBS="requests sqlalchemy tweepy"

cd ${WORKING_DIR}
source ${VIRTUAL_ENV_NAME}"/bin/activate"
if [ ! -d ${VIRTUAL_ENV_NAME} ] ; then
    virtualenv ${VIRTUAL_ENV_NAME}
fi
for libName in "${PYTHON_LIBS}"
do
    pip install ${libName}
done
