from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import docs.twitter_credentials



class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app();
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):  # If an id is not specified it will get your own timeline
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friend_list.append(friend);
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def publish_tweet(self,text):
        self.twitter_client.update_status(text)

    def tweet_image(self, message,filenames):
        if type(filenames) is not list:
            self.twitter_client.update_with_media(status=message , filename=filenames)
            return
        media_ids=[]
        for filename in filenames:
            res=self.twitter_client.media_upload(filename)
            media_ids.append(res.media_id)
        self.twitter_client.update_status(status=message,media_ids=media_ids)

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(docs.twitter_credentials.CONSUMER_KEY, docs.twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(docs.twitter_credentials.ACCESS_TOKEN, docs.twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, hashtag_list):
        # Twitter authentification and connection
        listener = TwitterListener()
        stream = Stream(self.twitter_authenticator.authenticate_twitter_app(), listener)
        stream.filter(track=hashtag_list)

class TwitterListener(StreamListener):

    def __init__(self, *fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.i = 0

    def on_data(self, data, filename):  # Méthode ovveridden
        try:
            file=open(filename,"a")
            file.write(data)
            self.i=self.i+1
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return self.i<5  # True keeps connection going , False kills connection

    def on_error(self, status):
        if status == 420:  # Returns 420 in case rate limit occurs
            return False
        print(status)


if __name__ == "__main__":
    # stockList=['^FCHI']
    # stocks=stockContainer()
    # stocks.get_stocks(stockList,"13-11-2019", "14-11-2019","d")
    # DF=stocks.conteneur
    # pd.set_option('display.max_columns',50)
    # f = pdr.DataReader(stockList, "av-daily", start=datetime(2019, 11, 10),end = datetime(2019, 11, 14),api_key = AvKey)
    #print(alois.get_home_timeline_tweets(1))
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hashtagList)
    streamer = TwitterStreamer()
    client = TwitterClient()
    # streamer.stream_tweets(hashtag_list=['SEC'])
    client.publish_tweet("Hello world")

