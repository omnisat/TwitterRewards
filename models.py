from tweepy.models import User, Status
import peewee
import datetime
import spacy
from helpers import pre_process_tweet
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_trf')
nlp.add_pipe('spacytextblob')

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
    date: datetime.datetime = peewee.DateTimeField()
    text: str = peewee.CharField()
    source: str = peewee.CharField()
    lang: str = peewee.CharField()
    urls: str = peewee.TextField(null=True)
    is_quote_status: bool = peewee.BooleanField()
    in_reply_to_screen_name: str = peewee.CharField(null=True)
    quote_count: int = peewee.IntegerField()
    reply_count: int = peewee.IntegerField()
    retweet_count: int = peewee.IntegerField()
    favorite_count: int = peewee.IntegerField()
    author_name: str = peewee.CharField()
    author = peewee.ForeignKeyField(CurvanceUser, backref='all_tweets')

    class Meta:
        database = db

    def individual_tweet_score(self) -> float:
        text = pre_process_tweet(self.text)
        sentiment = nlp(text)
        polarity = sentiment._.polarity
        nlp_score = 1 + max(0, polarity)  # gives max a 50% bonus

        if self.lang == 'und' and (self.favorite_count + self.quote_count + self.retweet_count) == 0:
            # Assigning 0 to undefined language with 0 engagement Mostly monolitic emoticons
            return 0

        score = 1
        score += self.favorite_count + 1.5 * self.quote_count + 2 * self.retweet_count

        return score * nlp_score
