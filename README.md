## A script to parse, store and rate tweets for Curvance Rewards. 

In order to use the client, you should place a `logs.txt` file at the root of the repository containing your api keys and the dev environment label.  
You should be able to find/create all of those in your twitter developer portal : https://developer.twitter.com/en/portal/dashboard 
Here's a sample that you can use (only the order counts) :
```
apikey=
secret=
bearer_token=
access_token=
access_token_secret=
label=
```


### Some notes about the twitter API : 

For now, Twitter V2 API doesn't seem to return details about queried tweets besides their id if you don't have the academic research level. No account id, no timestamps, nothing. 


Twitter V1.1 API should be used instead despite having lower limits for free-tier accounts.
See limits and pricing here : https://developer.twitter.com/en/pricing/search-30day 


When making a Twitter query, consider the operators/filters listed here : https://developer.twitter.com/en/docs/twitter-api/enterprise/rules-and-filtering/operators-by-product
and acknowledge that the free tier is labeled as "Sandbox"


Some Useful links : 

https://developer.twitter.com/en/docs/twitter-api/search-overview

https://docs.tweepy.org/en/stable/api.html#premium-search-apis

https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet


### Updates 31/12/21 : Some notes about pickled object, peewee and the sqlite database

The `main.py` now works correctly.
It will create a pickled object from a sample request from twitter containing 10 tweets. This is used to debug the creation and update of the database.

The reason the pickled object hasn't been uploaded to github is that you should not load pickled objects from untrusted sources. 

Here, you will create and store your own so you won't use all your credits for twitter API calls (which are very limited), and also be sure won't get hacked by me :D 

Don't hesitate to use the open source sqlite browser to inspect the .sqlite file that the Client will generate https://sqlitebrowser.org/

Don't hesitate to run main.py multiple times or delete the database to check for errors, but for now, it works ! 

