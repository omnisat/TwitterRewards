from client import Tw
import os.path
from tweepy.models import ResultSet
from models import db, CurvanceUser, CurvanceTweet
import pickle

# Uncomment this if you want to see SQL queries :

# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

# Main script to load / update tweets from DB/Client, create CurvanceUsers objects, and compute score using relevant
# methods
# Weight the sum of tweets scores by a User score that should be normalized among all users that participated.

MAX_CVE_TO_DISTRIBUTE = 10000

client = Tw()

if not os.path.isfile('response_sample'):
    r = client.search_up_to_30_days(query='"@Curvance"', max_results=100, days_back=1)
    file = open('response_sample', 'wb')
    pickle.dump(r, file)
    file.close()

file = open('response_sample', 'rb')
response_sample: ResultSet = pickle.load(file)
file.close()

client.store_response_to_db(response_sample)


class CurvanceScoreDistributor:
    def __init__(self):
        self.all_curvance_users = [cve_user for cve_user in CurvanceUser.select()]
        self.max_tweets_per_day_allowed = 5
        self.n_followers_sample = []
        self.add_users_statistics()

    def compute(self):
        curvance_user: CurvanceUser
        tweet: CurvanceTweet

        for curvance_user in self.all_curvance_users:
            all_tweets_from_user_sorted_by_date = [tweet for tweet in
                                                   curvance_user.all_tweets.order_by(CurvanceTweet.date.asc())]
            sum_of_individual_tweet_score = 0
            number_of_tweet_this_day = 0
            this_day_scores = []
            this_day_date = all_tweets_from_user_sorted_by_date[0].date.date()

            for tweet in all_tweets_from_user_sorted_by_date:
                individual_tweet_score = tweet.individual_tweet_score()

                if tweet.date.date() == this_day_date:
                    number_of_tweet_this_day += 1
                    this_day_scores.append(individual_tweet_score)
                if tweet.date.date() > this_day_date:
                    sum_of_individual_tweet_score += self.add_best_scores_of_the_day(this_day_scores)
                    this_day_date = tweet.date.date()
                    this_day_scores = [individual_tweet_score]
                    number_of_tweet_this_day = 1

            user_score = curvance_user.compute_user_score()
            curvance_user.final_user_score = user_score * sum_of_individual_tweet_score
            print(curvance_user.user_tag + ' score : ', curvance_user.user_score)

    def add_best_scores_of_the_day(self, this_day_scores: list):
        scores = this_day_scores
        scores.sort(reverse=True)
        return sum(scores[:self.max_tweets_per_day_allowed])

    def add_users_statistics(self):
        for user in self.all_curvance_users:
            self.n_followers_sample.append(user.followers_count)

