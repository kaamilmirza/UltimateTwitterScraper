import tweepy
import pandas as pd
from sys import stdin
import authenticate

auth = authenticate.auth
auth.set_access_token(authenticate.twitterAPIAT,authenticate.twitterAPIATS)

twetterApi = tweepy.API(auth, wait_on_rate_limit=True)

print("""This py file helps you the most frequent @ tweets sent out by 
particular users. You can enter their usernames and find their frequent @s """)
print("Now you can enter usernames in multiple lines by pressing enter and when done, press enter one last time: ")




def main(username_list):
    for username in username_list:
        mention_list = []
        try:
            numberOfTweets = input("The number of tweets you want to be picked for {}:".format(username))
        except ValueError:
            print("Please enter integers only!")

        print("Please wait...tweets of: {} are been picked.".format(username))
        try:
            for tweet in tweepy.Cursor(twetterApi.user_timeline,
                                       screen_name=username,
                                       count=None,
                                       since_id=None,
                                       max_id=None,
                                       trim_user=True,
                                       exclude_replies=False,
                                       contributor_details=False,
                                       include_entities=True
                                       ).items(int(numberOfTweets)):

                try:
                    user_mentioned = tweet.entities['user_mentions'][0]['screen_name']
                    mention_list.append(user_mentioned)
                except IndexError:
                    pass
            print("DATA FOR USER:{}".format(username))
            print("")
            Data_perUSER(mention_list)
            print("")
        except tweepy.error.TweepError:
            print("Some error from Twitter,please try again with correct inputs")


def Data_perUSER(mention_list):
    elements_count = {}
    for element in mention_list:
        # checking whether it is in the dict or not
        if element in elements_count:
            # incerementing the count by 1
            elements_count[element] += 1
        else:
            # setting the count to 1
            elements_count[element] = 1
    d = []

    for key, values in elements_count.items():
        d.append([key, values])
    choice = input("If you want just top mentions of dataframe enter 1 :")
    df = pd.DataFrame(d, columns=['Names of the users', 'Number of times they have been mentioned'])
    try:
        if choice == str(1):
            sorted_df = df.sort_values(by="Number of times they have been mentioned", ascending=False)
            print(sorted_df.head(10))
        else:
            with pd.option_context('display.max_rows', None, 'display.max_columns',
                                   None):  # more options can be specified also
                sorted_df = df.sort_values(by="Number of times they have been mentioned", ascending=False)

                print(sorted_df)
    except ValueError:
        with pd.option_context('display.max_rows', None, 'display.max_columns',None):
            # more options can be specified also
            sorted_df = df.sort_values(by="Number of times they have been mentioned", ascending=False)
            print(sorted_df)

def taking_input():
    username_list = []
    for line in stdin:
        username_list.append(line.rstrip())
        if line == '\n': # If empty string is read then stop the loop
            break
    username_list.pop()
    print("These are the usernames you have entered:")
    for name in username_list:
        print(name)

    main(username_list)

taking_input()
