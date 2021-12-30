from tweepy.models import ResultSet, User, Status
import datetime


# Models for Users and Tweets
# Theses classes should be derived of Base class of an ORM afterwards
# They also need more methods to compute relevant metrics

class CurvanceUser:
    def __init__(self, tweepy_user_object: User):
        self.user_id: int = tweepy_user_object.id
        self.user_tag: str = tweepy_user_object.screen_name
        self.account_creation_date: datetime.datetime = tweepy_user_object.created_at
        self.followers_count: int = tweepy_user_object.followers_count
        self.friends_count: int = tweepy_user_object.friends_count
        self.statuses_count: int = tweepy_user_object.statuses_count
        self.verified: bool = tweepy_user_object.verified
        self.curvance_tweets: dict = {}

    def add_tweet(self, tweepy_tweet_object: Status):
        curvance_tweet = CurvanceTweet(tweepy_tweet_object)
        self.curvance_tweets[curvance_tweet.tweet_id] = curvance_tweet

    def compute_score(self):
        # Loop over all tweets and call CurvanceTweet.individual_score()
        # Use frequency analysis / Count tweets to put a hard cap of tweets per period

        pass


class CurvanceTweet:
    def __init__(self, tweepy_tweet_object: Status):
        self.id: int = tweepy_tweet_object.id
        self.date: datetime.datetime = tweepy_tweet_object.created_at
        self.text: str = tweepy_tweet_object.text
        self.source: str = tweepy_tweet_object.source
        self.is_quote_status: bool = tweepy_tweet_object.is_quote_status
        self.in_reply_to_screen_name: str = tweepy_tweet_object.in_reply_to_screen_name
        self.quote_count: int = tweepy_tweet_object.quote_count
        self.reply_count: int = tweepy_tweet_object.reply_count
        self.retweet_count: int = tweepy_tweet_object.retweet_count
        self.favorite_count: int = tweepy_tweet_object.favorite_count

    def individual_tweet_score(self) -> float:
        pass
