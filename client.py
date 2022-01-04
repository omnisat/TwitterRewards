import tweepy
import datetime
from tweepy.models import ResultSet, User, Status
from models import CurvanceTweet, CurvanceUser, db
from peewee import DoesNotExist

from helpers import convert_user_to_dict, convert_tweet_to_dict

# Here is the client class that should parse all relevant tweets within the last 30 days. Iteration on the response
# should be done to create models objects that can be store into a sqlite database using an ORM.
#
import logging


# logger = logging.getLogger()
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


class Tw:
    def __init__(self):
        self.file = open("logs.txt", 'r')
        self.public_key = self.file.readline().split('\n')[0].split('=')[1]
        self.secret_key = self.file.readline().split('\n')[0].split('=')[1]
        self.bearer_token = self.file.readline().split('\n')[0].split('=')[1]
        self.access_token = self.file.readline().split('\n')[0].split('=')[1]
        self.access_token_secret = self.file.readline().split('\n')[0].split('=')[1]
        self.environment_label = self.file.readline().split('\n')[0].split('=')[1]
        self.file.close()
        self.v2_client = tweepy.Client(bearer_token=self.bearer_token, consumer_key=self.public_key,
                                       consumer_secret=self.secret_key, access_token=self.access_token,
                                       access_token_secret=self.access_token_secret)
        self.auth = tweepy.OAuthHandler(consumer_key=self.public_key, consumer_secret=self.secret_key)
        self.auth.set_access_token(key=self.access_token, secret=self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.db = db
        self.db.create_tables([CurvanceUser, CurvanceTweet])

    def search_last_7_days(self, query: str):
        # Issues with V2 API as of end of 2021 : no information about each tweet for non-academical accounts
        response = self.v2_client.search_recent_tweets(query=query, user_auth=True)
        # next_token = r.meta['next_token']
        return response

    def search_up_to_30_days(self, query: str, max_results=10, days_back: int = 1) -> ResultSet:
        result_set = ResultSet()

        if 1 <= days_back <= 30:
            from_date = (datetime.datetime.utcnow() - datetime.timedelta(days=days_back)).strftime('%Y%m%d%H%M')
            response = self.api.search_30_day(label=self.environment_label, query=query, maxResults=max_results,
                                              fromDate=from_date)
            token = response[1]
            result_set = result_set + response[0]
            while token is not None:
                response = self.api.search_30_day(label=self.environment_label, query=query, maxResults=max_results,
                                                  fromDate=from_date, next=token)
                token = response[1]
                if type(response[0]) == ResultSet:
                    result_set = result_set + response[0]
                elif type(response[0][0]) == ResultSet:
                    result_set = result_set + response[0][0]

        else:
            raise ValueError("days_back must be an integer between 1 and 30")

        return result_set

    def store_response_to_db(self, response: ResultSet):
        for tweet in response:
            try:
                curvance_user = CurvanceUser.get_by_id(tweet.user.id)
                CurvanceUser.update(**convert_user_to_dict(tweet.user))
            except DoesNotExist:
                curvance_user = CurvanceUser.create(**convert_user_to_dict(tweet.user))
            try:
                CurvanceTweet.get_by_id(tweet.id)
                CurvanceTweet.update(**convert_tweet_to_dict(tweet), author=curvance_user)
            except DoesNotExist:
                CurvanceTweet.create(**convert_tweet_to_dict(tweet), author=curvance_user)

        pass


if __name__ == '__main__':
    c = Tw()
    r = c.search_up_to_30_days('"@Curvance"', max_results=100, days_back=2)
