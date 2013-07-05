
# Change the following for your env.
WORKING_DIR='/path/to/meetup-spreader-python'
SECRETS_PATH='/path/to/secrets.sh'


# This stuff is to set up the application environment.
VIRTUAL_ENV_NAME='meetup-spreader-virtualenv'
PYTHON_LIBS="requests sqlalchemy tweepy"

cd ${WORKING_DIR}
source ${SECRETS_PATH}
source ${VIRTUAL_ENV_NAME}"/bin/activate"
if [ ! -d ${VIRTUAL_ENV_NAME} ] ; then
    virtualenv ${VIRTUAL_ENV_NAME}
fi
for libName in "${PYTHON_LIBS}"
do
    pip install ${libName}
done
