from tweepy.models import Status, User
import re
import contractions
from spacy.lang.en.stop_words import STOP_WORDS


def convert_tweet_to_dict(tweet: Status):
    tweet_dict = {}
    tweet_dict['id'] = tweet.id
    tweet_dict['date'] = tweet.created_at
    tweet_dict['text'] = tweet.text
    tweet_dict['lang'] = tweet.lang
    tweet_dict['urls'] = '\n'.join([url['expanded_url'] for url in tweet.entities['urls']])
    tweet_dict['author_name'] = tweet.user.screen_name
    tweet_dict['source'] = tweet.source
    tweet_dict['is_quote_status'] = tweet.is_quote_status
    tweet_dict['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
    tweet_dict['quote_count'] = tweet.quote_count
    tweet_dict['reply_count'] = tweet.reply_count
    tweet_dict['retweet_count'] = tweet.retweet_count
    tweet_dict['favorite_count'] = tweet.favorite_count

    return tweet_dict


def convert_user_to_dict(user: User):
    user_dict = {}
    user_dict['user_id'] = user.id
    user_dict['user_tag'] = user.screen_name
    user_dict['account_creation_date'] = user.created_at
    user_dict['followers_count'] = user.followers_count
    user_dict['friends_count'] = user.friends_count
    user_dict['statuses_count'] = user.statuses_count
    user_dict['verified'] = user.verified

    return user_dict


def pre_process_tweet(tweet_text: str):
    text = tweet_text.lower()
    text = re.sub(r'([A-Za-z0-9+_]+@[A-Za-z0-9+_]+\.[A-Za-z0-9+_]+)', '', text)  # remove emails
    text = re.sub(r'https?://[^\s<>"]+|www\.[^\s<>"]+', '', text)  # remove links
    text = re.sub("@[A-Za-z0-9_]+", "", text)  # remove mentions
    text = re.sub("#[A-Za-z0-9_]+", "", text)  # remove hashtags
    text = re.sub('rt', '', text)  # remove RT
    text = contractions.fix(text)  # expand contractions
    text = re.sub('[^A-Z a-z 0-9-]+', '', text)  # remove special characters
    text = " ".join(text.split())  # remove double spaces
    text = " ".join(t for t in text.split() if t not in STOP_WORDS)  # remove stop words

    return text
