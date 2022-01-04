from client import Tw
import os.path
from tweepy.models import ResultSet
from models import db, CurvanceUser, CurvanceTweet
import pickle

# Main script to load / update tweets from DB/Client, create CurvanceUsers objects, and compute score using relevant
# methods
# Weight the sum of tweets scores by a User score that should be normalized among all users that participated.

MAX_CVE_TO_DISTRIBUTE = 10000

# Uncomment this if you want to see SQL queries :

# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

client = Tw()

if not os.path.isfile('response_sample'):
    r = client.search_up_to_30_days(query='"@Curvance"', max_results=100, days_back=1)
    file = open('response_sample', 'wb')
    pickle.dump(r, file)
    file.close()

file = open('response_sample', 'rb')
response_sample: ResultSet = pickle.load(file)
file.close()

# client.store_response_to_db(response_sample)
