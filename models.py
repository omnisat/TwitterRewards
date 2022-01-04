from tweepy.models import User, Status
import peewee
import datetime

# Models for Users and Tweets
# Theses classes should be derived of Base class of an ORM afterwards
# They also need more methods to compute relevant metrics


db = peewee.SqliteDatabase('curvance_twitter.sqlite', pragmas={'foreign_keys': 1})


class CurvanceUser(peewee.Model):
    user_id: int = peewee.IntegerField(primary_key=True, unique=True)
    user_tag: str = peewee.CharField()
    account_creation_date: datetime.datetime = peewee.DateField()
    followers_count: int = peewee.IntegerField()
    friends_count: int = peewee.IntegerField()
    statuses_count: int = peewee.IntegerField()
    verified: bool = peewee.BooleanField()
    final_user_score = 0

    class Meta:
        database = db

    def compute_user_score(self):
        # Score multiplier from age and followers

        score = 1

        return score


class CurvanceTweet(peewee.Model):
    id: int = peewee.IntegerField(primary_key=True, unique=True)
    date: datetime.datetime = peewee.DateField()
    text: str = peewee.CharField()
    source: str = peewee.CharField()
    is_quote_status: bool = peewee.BooleanField()
    in_reply_to_screen_name: str = peewee.CharField(null=True)
    quote_count: int = peewee.IntegerField()
    reply_count: int = peewee.IntegerField()
    retweet_count: int = peewee.IntegerField()
    favorite_count: int = peewee.IntegerField()
    author = peewee.ForeignKeyField(CurvanceUser, backref='all_tweets')

    class Meta:
        database = db

    def individual_tweet_score(self) -> float:
        score = 1
        score += self.favorite_count + 1.5 * self.quote_count + 2 * self.retweet_count

        return score
