import tweepy
import authenticate
import urllib.request
import socket
import os
socket.getaddrinfo('localhost', 8080) #sometimes crashes and gives weird errors this somehow fixed it

#GETTING AUTHENTICATION DATA REQ. WITH TWITTER API
auth = authenticate.auth
auth.set_access_token(authenticate.twitterAPIAT,authenticate.twitterAPIATS)
twetterApi = tweepy.API(auth, wait_on_rate_limit=True)

def taking_input():
    twitterAccount = input("The username you want to get the media for [photos]:")
    try:
        numberOfTweets = input("The number of tweets you want to be picked:")
    except ValueError:
        print("Please enter only integer values!")
    main(twitterAccount,numberOfTweets)

def main(twitterAccount,numberOfTweets):
    tweets = tweepy.Cursor(twetterApi.user_timeline,
                           screen_name=twitterAccount,
                           count=None,
                           since_id=None,
                           max_id=None,
                           trim_user=True,
                           exclude_replies=True,
                           contributor_details=False,
                           include_entities=True
                           ).items(int(numberOfTweets))
    count = 0
    try:
        os.mkdir("./Images")
    except FileExistsError:
        pass

    print("Please wait...grabbing tweets of {}".format(twitterAccount))
    for tweet in tweets:

                    #not all tweets will have media url, so lets skip them
                    try:
                         url = tweet.entities['media'][0]['media_url']
                         urllib.request.urlretrieve(url, "Images/" + str(count) + ".jpg")
                         count = count+1

                    except (NameError, KeyError):
                            #we dont want to have any entries without the media_url so lets do nothing
                            pass

taking_input()