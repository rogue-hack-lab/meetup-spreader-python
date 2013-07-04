
# Change the following for your env.
WORKING_DIR='/home/fran/random/rhlsquid/rhl-twitter-time'
SECRETS_PATH='/home/fran/random/rhlsquid/secrets/secrets.sh'
VIRTUAL_ENV_NAME='twitterTimeVirtualEnv'


# This stuff is to set up the application environment.
PYTHON_LIBS="requests sqlalchemy tweepy"

cd ${WORKING_DIR}
source ${SECRETS_PATH}
if [ ! -d ${VIRTUAL_ENV_NAME} ] ; then
    virtualenv ${VIRTUAL_ENV_NAME}
fi
for libName in "${PYTHON_LIBS}"
do
    pip install ${libName}
done
source ${VIRTUAL_ENV_NAME}"/bin/activate"

