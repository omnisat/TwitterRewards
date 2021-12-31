import tweepy
from tweepy.models import ResultSet, User, Status
from models import CurvanceTweet, CurvanceUser, db
from helpers import convert_user_to_dict, convert_tweet_to_dict


# Here is the client class that should parse all relevant tweets within the last 30 days. Iteration on the response
# should be done to create models objects that can be store into a sqlite database using an ORM.
#
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

    def search_last_30_days(self, query: str, max_results=10) -> ResultSet:
        response = self.api.search_30_day(label=self.environment_label, query=query, maxResults=max_results)
        return response

    def store_response_to_db(self, response: ResultSet):
        for tweet in response:
            curvance_user = CurvanceUser.get_or_create(**convert_user_to_dict(tweet.user))[0]

            CurvanceTweet.get_or_create(**convert_tweet_to_dict(tweet), author=curvance_user)
        pass
