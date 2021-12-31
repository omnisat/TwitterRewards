from tweepy.models import Status, User


def convert_tweet_to_dict(tweet: Status):
    tweet_dict = {}
    tweet_dict['id'] = tweet.id
    tweet_dict['date'] = tweet.created_at
    tweet_dict['text'] = tweet.text
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
