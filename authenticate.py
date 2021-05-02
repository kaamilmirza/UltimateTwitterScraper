import tweepy
import pandas as pd
config = pd.read_csv("./config.csv")
twitterAPIkey = config['twitterApiKey'][0]
twitterAPIS = config['twitterApiSecret'][0]
twitterAPIAT = config['twitterApiAccessToken'][0]
twitterAPIATS = config['twitterApiAccessTokenSecret'][0]

auth = tweepy.OAuthHandler(twitterAPIkey, twitterAPIS)
