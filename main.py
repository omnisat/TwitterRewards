import pandas as pd
import numpy as np

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
        self.n_followers_percentiles = pd.Series(dtype=float)
        self.engagement_percentiles = pd.Series(dtype=float)

        self.percentiles_array = np.linspace(0, 1, 100)
        self.add_users_statistics()
        self.results = []

    def compute_scores(self):
        curvance_user: CurvanceUser
        tweet: CurvanceTweet

        for curvance_user in self.all_curvance_users:
            all_tweets_from_user_sorted_by_date = [tweet for tweet in
                                                   curvance_user.all_tweets.order_by(CurvanceTweet.date.asc())]
            sum_of_individual_tweet_score = 0
            this_day_scores = []
            this_day_date = pd.to_datetime(all_tweets_from_user_sorted_by_date[0].date).to_pydatetime().date()

            for tweet in all_tweets_from_user_sorted_by_date:

                individual_tweet_score = tweet.individual_tweet_score(
                    percentile_score=self.get_percentile_engagement_score(tweet.get_engagement_score()))
                tweet_date = pd.to_datetime(tweet.date).to_pydatetime().date()

                if tweet_date == this_day_date:
                    this_day_scores.append(individual_tweet_score)
                if tweet_date > this_day_date:
                    sum_of_individual_tweet_score += self.add_best_scores_of_the_day(this_day_scores)
                    this_day_date = tweet_date
                    this_day_scores = [individual_tweet_score]
                if tweet.id == all_tweets_from_user_sorted_by_date[-1].id:
                    sum_of_individual_tweet_score += self.add_best_scores_of_the_day(this_day_scores)

            percentile_score = self.get_percentile_user_score(n_follower=curvance_user.followers_count)
            user_score = curvance_user.compute_user_score(percentile_score=percentile_score)

            curvance_user.final_user_score = user_score * sum_of_individual_tweet_score

            self.results.append([curvance_user.user_tag, curvance_user.final_user_score])
            if curvance_user.final_user_score > 0:
                print(curvance_user.user_tag + ' score (user*tweets) : ', user_score, '*',
                      sum_of_individual_tweet_score,
                      " = ", curvance_user.final_user_score)

        return self.results

    def add_best_scores_of_the_day(self, this_day_scores: list) -> float:
        scores = this_day_scores
        scores.sort(reverse=True)
        return sum(scores[:self.max_tweets_per_day_allowed])

    def add_users_statistics(self) -> None:
        n_follower_sample = []
        engagement_sample = []
        tweet: CurvanceTweet
        for user in self.all_curvance_users:
            n_follower_sample.append(user.followers_count)
            tweets = [tweet for tweet in user.all_tweets]
            for tweet in tweets:
                if tweet.is_passing_filter():
                    engagement_score = tweet.get_engagement_score()
                    if engagement_score > 0:
                        engagement_sample.append(engagement_score)

        self.engagement_percentiles = pd.Series(engagement_sample).describe(percentiles=self.percentiles_array)[4:-1]
        self.n_followers_percentiles = pd.Series(n_follower_sample).describe(percentiles=self.percentiles_array)[4:-1]

    def get_percentile_user_score(self, n_follower: int) -> float:
        """
        Returns a value between 0 and 1 based on percentiles. If you have more followers than 50% of people, returns 0.5
        If you have more followers than 10% of people, returns 0.1. If more than 90% returns 0.9.
        Returns 0 if 0 followers and a minimum of self.percentile_step if more than 0 follower.
        :param n_follower:
        :return:
        """
        index = np.searchsorted(self.n_followers_percentiles, n_follower, side='right')
        if n_follower == 0:
            return 0
        elif index < self.percentiles_array.shape[0]:
            return self.percentiles_array[index]
        elif index == self.percentiles_array.shape[0]:
            return 1

    def get_percentile_engagement_score(self, engagement_score: int) -> float:
        index = np.searchsorted(self.engagement_percentiles, engagement_score, side='right')
        if engagement_score == 0:
            return 0
        elif index < self.percentiles_array.shape[0]:
            return self.percentiles_array[index]
        elif index == self.percentiles_array.shape[0]:
            return 1


rewards = CurvanceScoreDistributor()
# rewards.compute_scores()
