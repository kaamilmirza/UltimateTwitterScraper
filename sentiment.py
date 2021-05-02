import tweepy
from textblob import TextBlob
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import authenticate
import pandas as pd

auth = authenticate.auth
auth.set_access_token(authenticate.twitterAPIAT,authenticate.twitterAPIATS)
twetterApi = tweepy.API(auth, wait_on_rate_limit=True)

twitterAccount = input("The username you want  to run sentiment analysis on:")
numberOfTweets = input("The number of tweets:")
tweets = tweepy.Cursor(twetterApi.user_timeline,
                       screen_name=twitterAccount,
                       count=None,
                       since_id=None,
                       max_id=None,
                       trim_user=True,
                       exclude_replies=True,
                       contributor_details=False,
                       include_entities=False
                       ).items(int(numberOfTweets))

df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweet'])


# Cleaning the tweets

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


def getTextSubjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity


def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity


df['Subjectivity'] = df['Tweet'].apply(getTextSubjectivity)
df['Polarity'] = df['Tweet'].apply(getTextPolarity)

df = df.drop(df[df['Tweet'] == ''].index)


# negative, natural, positive analysis
def getTextAnalysis(a):
    if a < 0:
        return "Negative"
    elif a == 0:
        return "Neutral"
    else:
        return "Positive"


df['Score'] = df['Polarity'].apply(getTextAnalysis)
positive = df[df['Score'] == 'Positive']

print(str(positive.shape[0] / (df.shape[0]) * 100) + " % of positive tweets")
labels = df.groupby('Score').count().index.values

values = df.groupby('Score').size().values

plt.bar(labels, values)
objective = df[df['Subjectivity'] == 0]
plt.show()

print(str(objective.shape[0] / (df.shape[0]) * 100) + " % of objective tweets")
# Creating a word cloud

words = ' '.join([tweet for tweet in df['Tweet']])
stop_words = ['https'] + list(STOPWORDS)
# noinspection PyTypeChecker
wordCloud = WordCloud(width=600, height=400, stopwords=stop_words).generate(words)
plt.imshow(wordCloud)
plt.show()
