def main():
    print("""
            ________________THE TWITTER BOT___________________
            1) Run sentiment analysis of the twitter account 
            and create a worldcloud for tweets
            2) Finding mutual follows of multiple accounts 
            3) Get images of a twitter account
            4) Find top mentions by multiple accounts
            5) Find most liked tweet and most retweeted tweet 
            of multiple accounts
            """)
    choice = input("Enter your choice: (integer value)")
    try:
        if choice == str(1):
            import sentiment
        if choice == str(2):
            import mutualfollows
        if choice == str(3):
            import imagedata
        if choice == str(4):
            import topmentions
        if choice == str(5):
            import mostlikedtweet
    except ValueError:
        print("Please enter only integer values ")

if __name__ == '__main__':
    main()



