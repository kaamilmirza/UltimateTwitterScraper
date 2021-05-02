import tweepy
import authenticate
from sys import stdin
import socket
socket.getaddrinfo('localhost', 8080) #sometimes crashes and gives weird errors this somehow fixed it

auth = authenticate.auth
auth.set_access_token(authenticate.twitterAPIAT,authenticate.twitterAPIATS)

twetterApi = tweepy.API(auth, wait_on_rate_limit=True)
api = tweepy.API(auth, wait_on_rate_limit=True)
print("""
This py file allows you to find mutual follows between multiple accounts
Enter one username per line and when done press enter on a blank like and wait :)
""")
print("Now you can enter usernames in multiple lines by pressing enter: ")

username_list = []
def taking_input():
    for line in stdin:
        username_list.append(line.rstrip())
        if line == '\n': # If empty string is read then stop the loop
            break
    username_list.pop()
    print("These are the usernames you have entered:")
    for name in username_list:
        print(name)
    main()

def main():
    main_list = []
    count = 0
    for username in username_list:
        print("Please wait.....getting follows of:",username)
        for friends in tweepy.Cursor(api.friends_ids,username).items():
            main_list.append(api.get_user(friends).screen_name)
        print("End of user :" + username)
    mutual = []
    checked =[]
    for x in main_list:
        if main_list.count(x) >= len(username_list) and x not in mutual:
            mutual.append(x)
    print(mutual)

taking_input()








