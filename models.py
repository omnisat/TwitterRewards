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

    def compute_user_score(self, percentile_score: float):
        # Score multiplier from age and followers
        assert 0 <= percentile_score <= 1

        score = 1 * (1 + percentile_score)

        return score


class CurvanceTweet(peewee.Model):
    id: int = peewee.IntegerField(primary_key=True, unique=True)
    tweet_link: str = peewee.CharField()
    date: datetime.datetime = peewee.DateTimeField()
    author_name: str = peewee.CharField()
    text: str = peewee.CharField()
    lang: str = peewee.CharField()
    urls: str = peewee.TextField(null=True)
    has_media: bool = peewee.BooleanField(default=False)
    is_quote_status: bool = peewee.BooleanField()
    in_reply_to_screen_name: str = peewee.CharField(null=True)
    quote_count: int = peewee.IntegerField()
    reply_count: int = peewee.IntegerField()
    retweet_count: int = peewee.IntegerField()
    favorite_count: int = peewee.IntegerField()
    author = peewee.ForeignKeyField(CurvanceUser, backref='all_tweets')

    class Meta:
        database = db

    def individual_tweet_score(self, percentile_score) -> float:
        # if self.lang == 'und' and (self.favorite_count + self.quote_count + self.retweet_count + self.reply_count) == 0:
        #     # Assigning 0 to undefined language with 0 engagement Mostly monolitic emoticons
        #     print('returning 0')
        #     return 0

        if not self.is_passing_filter():
            return 0

        text = pre_process_tweet(self.text)

        sentiment = nlp(text)
        polarity = sentiment._.polarity
        nlp_score = 1 + 2 * max(0, polarity)  # gives max a 200% bonus

        engagement_score = 1 + (1 + percentile_score)

        print('tag: ', self.author_name, ' text :', text, ' | nlp score : ', nlp_score, 'total : ',
              str(engagement_score * nlp_score),
              ' https://twitter.com/i/web/status/' + str(self.id))

        return engagement_score * nlp_score

    def get_engagement_score(self):
        score = self.favorite_count + self.quote_count + self.retweet_count
        return score

    def is_passing_filter(self) -> bool:
        text_clean = pre_process_tweet(self.text)
        if len(text_clean.split()) == 1 and text_clean[-3:] == 'eth':
            # 0 to tweets contaning only an .eth address'
            return False
        elif len(text_clean.split()) == 0 and self.has_media is False and 'curvance' not in self.urls:
            # print('clean is 0:', self)
            return False
        else:
            return True

    def __str__(self):
        return self.author_name + ' | ' + self.text.replace('\n', ' ') + ' | https://twitter.com/i/web/status/' + str(
            self.id) + ' | ' + self.urls
