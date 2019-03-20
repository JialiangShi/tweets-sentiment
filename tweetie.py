import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.read().strip().split(',')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    consumer_key, consumer_secret, \
    access_token, access_token_secret \
        = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """

    tweets = []

    new_tweets = api.user_timeline(screen_name=name, count = 100, tweet_mode="extended")
    sid = SentimentIntensityAnalyzer()
    for tweet in new_tweets:
        t = {}
        t['id'] = tweet.id
        t['created'] = tweet.created_at
        t['retweeted'] = tweet.retweet_count
        t['text'] = tweet.full_text
        t['hashtags'] = tweet.entities['hashtags']
        t['urls'] = tweet.entities['urls']
        t['mentions'] = tweet.entities['user_mentions']
        t['score'] = sid.polarity_scores(tweet.full_text)['compound']
        tweets.append(t)

    dic = {}
    dic['user'] = name
    dic['count'] = len(tweets)
    dic['tweets'] = tweets
    return dic


def fetch_following(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    #user = api.get_user(name)
    #friends = user.friends()
    #friendsID = [f.id for f in friends]
    friendsID = api.friends_ids(name)
    following = []
    for i in friendsID:
        u = api.get_user(i)
        dic = {}
        dic['user'] = u.name
        dic['screen_name'] = u.screen_name
        dic['followers'] = u.followers_count
        dic['created'] = u.created_at
        dic['image'] = u.profile_image_url
        following.append(dic)

    return following
