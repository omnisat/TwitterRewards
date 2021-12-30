# A script to parse, store and rate tweets for Curvance Rewards. 

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


Some notes about twitter API : 

For now, Twitter V2 API doesn't seem to return details about queried tweets besides their id if you don't have the academic research level. No account id, no timestamps, nothing. 


Twitter V1.1 API should be used instead despite having lower limits for free-tier accounts.
See limits and pricing here : https://developer.twitter.com/en/pricing/search-30day 


When making a Twitter query, consider the operators/filters listed here : https://developer.twitter.com/en/docs/twitter-api/enterprise/rules-and-filtering/operators-by-product
and acknowledge that the free tier is labeled as "Sandbox"


Some Useful links : 

https://developer.twitter.com/en/docs/twitter-api/search-overview

https://docs.tweepy.org/en/stable/api.html#premium-search-apis

https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet


