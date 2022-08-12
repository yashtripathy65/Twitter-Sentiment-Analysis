import tweepy as tp
import pandas as pd
import datetime as dt
from datetime import timedelta as td
from textblob import TextBlob as tb
from matplotlib import pyplot as plt
import twitter_credentials as twt
con_key = twt.con_key
con_key_secret = twt.con_key_secret
con_token = twt.con_token
con_token_secret = twt.con_token_secret
bearer_token = twt.bearer_token
auth = tp.OAuthHandler(con_key,con_key_secret)
auth.set_access_token(con_token,con_token_secret)
api = tp.API(auth)
client = tp.Client(consumer_key=con_key,consumer_secret=con_key_secret,access_token=con_token,access_token_secret=con_token_secret, bearer_token = bearer_token)
columns = ['user_id','tweet_id','created_at','tweet']
df = pd.DataFrame(columns=columns)
time = dt.datetime.now()
wd = input("ENTER THE KEYWORD TO BE ANALYSED \n")
word = ('#'+wd) or wd or (wd + 'is best') or (wd + 'is better') or (wd + 'is not good') or (wd + 'is worst')
def polarity(text):
    a = tb(text)
    return a.sentiment.polarity
def sentiment(arg):
    if arg>0:
        return 'positive'
    elif arg<0:
        return 'negative'
    elif arg == 0:
        return 'neutral'
time_end = dt.datetime.now() - td(hours = 6)
time_start = time_end - td(hours = 6)
while time_start > (time - td(days=6)):
    tweets = client.search_recent_tweets(query = word, start_time = time_start,end_time = time_end,tweet_fields ='created_at', expansions='author_id',max_results=100)
    for tweet in tweets.data:
        df = df.append({'user_id':tweet.author_id,'tweet_id':tweet.id,'created_at':tweet.created_at,'tweet':tweet.text}, ignore_index = True)
    time_start = time_start - td(hours = 6)
    time_end = time_end - td(hours = 6)
pd.options.display.max_rows = None
df1 = df.drop_duplicates(ignore_index=True)
df1['Polarity']= df1['tweet'].apply(polarity)
df1['Sentiment']= df1['Polarity'].apply(sentiment)
df2 = df1.groupby(["Sentiment"]).count()
df3 = df2.iloc[:,3]
# df3 = df3.transpose()
df4 = pd.DataFrame(df3)
# df4 = df4.transpose()
# df4['Total_Tweets'] = df4.sum(1)
# df4 = df4.transpose()

print("Total Tweets Searched = ", df1.shape[0])
print("")
print("Sentiment Analysis Table ",'\n',df4)
df4.plot(kind = 'pie',subplots = True)
plt.show()
