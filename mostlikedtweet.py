import tweepy
import pandas as pd
import re
from sys import stdin
import socket
import authenticate
socket.getaddrinfo('localhost', 8080)  # sometimes crashes and gives weird errors this somehow fixed it

auth = authenticate.auth
auth.set_access_token(authenticate.twitterAPIAT,authenticate.twitterAPIATS)

twetterApi = tweepy.API(auth, wait_on_rate_limit=True)

def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    # Remove hashtags
    txt = re.sub(r'#', '', txt)
    # Remove retweets:
    txt = re.sub(r'RT : ', '', txt)
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    return txt

print("The usernames you want to find likes for :")

def taking_input():
    username_list = []
    for line in stdin:
        username_list.append(line.rstrip())
        if line == '\n':  # If empty string is read then stop the loop
            break
    username_list.pop()
    main(username_list)

def main(username_list):
    count_tweet_list = []
    count_retweet_list = []
    for user in username_list:
        numberOfTweets = input("The number of tweets for user:{} you want to be picked:".format(user))
        print("Please wait...getting tweets of {}".format(user))
        for tweet in tweepy.Cursor(twetterApi.user_timeline,
                                   screen_name=user,
                                   since_id=None,
                                   max_id=None,
                                   trim_user=True,
                                   exclude_replies=True,
                                   contributor_details=False,
                                   include_entities=True
                                   ).items(int(numberOfTweets)):

            clean_tweet = cleanUpTweet(tweet._json['text'])
            liked_tweet_count = tweet._json['favorite_count']
            retweet_count = tweet._json['retweet_count']
            count_tweet_list.append([liked_tweet_count, clean_tweet])
            count_retweet_list.append([retweet_count,clean_tweet])

        df = pd.DataFrame(count_tweet_list, columns=['Number Of Likes', 'The tweets'])
        df_retweet = pd.DataFrame(count_retweet_list, columns=['Number of retweets', 'The tweets'])
        choice = input("If you want just top likes and retweets of dataframe enter 1 :")

        try:
            if choice == str(1):
                sorted_df = df.sort_values(by="Number Of Likes", ascending=False)
                sorted_retweet_df = df_retweet.sort_values(by="Number of retweets", ascending=False)
                print("The data regarding likes:")
                print(sorted_df.head(10))
                print("The data regarding retweets:")
                print(sorted_retweet_df.head(10))
            else:
                with pd.option_context('display.max_rows', None, 'display.max_columns',
                                       None):  # more options can be specified also
                    sorted_df = df.sort_values(by="Number Of Likes", ascending=False)
                    sorted_retweet_df = df.sort_values(by="Number of retweets", ascending=False)
                    print("The data regarding likes:")
                    print(sorted_df.head(10))
                    print("The data regarding retweets:")
                    print(sorted_retweet_df.head(10))
        except ValueError:
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                # more options can be specified also
                sorted_df = df.sort_values(by="Number Of Likes", ascending=False)
                sorted_retweet_df = df.sort_values(by="Number of retweets", ascending=False)
                print("The data regarding likes:")
                print(sorted_df.head(10))
                print("The data regarding retweets:")
                print(sorted_retweet_df.head(10))

taking_input()