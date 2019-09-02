#Importing Libraries required to run this program
import tweepy
import sys
from textblob import TextBlob

#Assign keys required to access the Twitter API
consumer_key = 'xxxxxxx'
consumer_secret = 'xxxxxxx'
access_token='xxxxxxx'
access_token_secret='xxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Function to print BMP Characters - not used in this program though
def decode_bmp(text):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    item=text.translate(non_bmp_map)+'\n\n'
    return item

#Sentiment Analysis using TextBlob
def tweets_sentiment_count(tweets_analysis):    
    count_positive=0
    count_negative=0
    count_neutral=0
    for i in tweets_analysis:
        if tweets_analysis[i]=='positive':
            count_positive+=1
        elif tweets_analysis[i]=='neutral':
            count_neutral+=1
        else:
            count_negative+=1
    count_sentiment={'count_positive':count_positive,'count_negative':count_negative,'count_neutral':count_neutral}
    return count_sentiment

def tweets_sentiment(tweets_dict):
    tweet_analysis={}
    for tweet in tweets_dict:
        analysis=TextBlob(tweets_dict[tweet])
        if analysis.sentiment.polarity>0:
            tweet_analysis[tweet]='positive'
        elif analysis.sentiment.polarity==0:
            tweet_analysis[tweet]='neutral'
        else:
            tweet_analysis[tweet]='negative'
        #print(tweets_dict[tweet]+": "+tweet_analysis[tweet]+"\n\n")
    return tweet_analysis

#Get Min ID:
def get_min_id(public_tweets):
    dict1={}
    for i in public_tweets:
        dict1[i]=i
    return min(dict1.values())

#The Main Program
count=int(input("Enter the number of tweets you wish to analyse(keep it below 5000): "))
movie_name=input("Enter Movie Hashtag: ")
temp=0
last_tweet_id=""
public_tweets={}

#Loop to gather more than 100 tweets, as Twitter API returns only 100 tweets per request.
while temp<count:
    if temp==0:
        if count<=100:
            temp_tweets = api.search(movie_name,count=count,tweet_mode="extended")
            for i in temp_tweets:
                public_tweets[i.id_str]=i.full_text
            temp+=count
            last_tweet_id=get_min_id(public_tweets)
        elif count>100:
            temp_tweets = api.search(movie_name,count=100,tweet_mode="extended")
            for i in temp_tweets:
                public_tweets[i.id_str]=i.full_text
            temp+=100
            last_tweet_id=get_min_id(public_tweets)
    elif temp>0:
        if count>100 and count-temp>100:
            temp_tweets = api.search(movie_name,count=100,tweet_mode="extended",max_id=last_tweet_id)
            for i in temp_tweets:
                public_tweets[i.id_str]=i.full_text
            temp+=100
            last_tweet_id=get_min_id(public_tweets)
        elif count>100 and count-temp<=100:
            temp_tweets = api.search(movie_name,count=count-temp,tweet_mode="extended",max_id=last_tweet_id)
            for i in temp_tweets:
                public_tweets[i.id_str]=i.full_text
            temp+=100
            last_tweet_id=get_min_id(public_tweets)

tweets_dict={}
i=1

#Gathering Tweets and their IDs into a dict
for tweet in public_tweets:
    tweets_dict[tweet]=public_tweets[tweet]
    tweets_dict[tweet]= ''.join(c for c in tweets_dict[tweet] if c <= '\uFFFF')
    print(str(i)+" "+tweets_dict[tweet]+"\n")
    i+=1

#Running the setiment query
count_sentiment=tweets_sentiment_count(tweets_sentiment(tweets_dict))

print('\nTotal Tweets Analyzed: '+str(i-1)) #i-1 will be equal to count

c_pos=round(100.00*count_sentiment['count_positive']/(i-1),2)
c_neu=round(100.00*count_sentiment['count_neutral']/(i-1),2)
c_neg=round(100.00*count_sentiment['count_negative']/(i-1),2)

print('Used Twitter API and Python to analyze the latest '+str(count)+' tweets with '+ movie_name +' hashtag. And this is what the audiences feel:\nSuperb: '+str(c_pos)+'%\nAverage: '+str(c_neu)+'%\nBad: '+str(c_neg)+'%')