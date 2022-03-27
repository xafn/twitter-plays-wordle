import tweepy
consumer_key = "iffHE4acYzTSccmS1zwTZmmT5"
consumer_secret = "CNo0YxXgxZ4u1JHuhUCH7JrIcsStNioWJh8Y5ZT5Ly90zQJirS"
access_token = "1503917778977366018-bmjXtYAqYemIdMAfp1CwZ6ih9E7WmK"
access_token_secret = "tm9ejhOa88hjm3uUOPxn1BPtanQRdsd5kunSLCTkR46c3"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)