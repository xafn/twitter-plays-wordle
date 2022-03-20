import tweepy, ssl, pandas, csv, re, random
from wordle import *

guess_list = open('avawords.txt').read().splitlines()

ssl._create_default_https_context = ssl._create_unverified_context

consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

name = 'WordleGame_Bot'
tweets_list= api.user_timeline(screen_name=name, count=1, exclude_replies=True)
recent_tweet = tweets_list[0]
tweet_id = recent_tweet.id_str

replies=[]
for tweet in tweepy.Cursor(api.search_tweets,q='to:'+name, result_type='popularity').items(250):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        if (tweet.in_reply_to_status_id_str==tweet_id):
            replies.append(tweet)

with open('replies.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=('ID', 'TEXT', 'LIKES'))
    csv_writer.writeheader()
    for tweet in replies:
        text = tweet.text.replace('@WordleGame_Bot ', '')
        text = text.replace('\n', ' ')
        text = text.lower()
        row = {'ID': tweet.id_str, 'TEXT': text, 'LIKES': tweet.favorite_count}
        if '\[' and ']' in text or len(text) == 5: #i see you @ThatOneCalculator this ones for you
            csv_writer.writerow(row)
    
df = pandas.read_csv('replies.csv')
df = df.sort_values('LIKES', ascending=False)
df.to_csv('replies.csv', index=False)  

df2 = pandas.read_csv('counter.csv')

if df2.at[0,'CURRENT_ROW'] == 7 or df2.at[0,'CURRENT_ROW'] == 0 or not bool(df2.at[0,'NOT_WIN']):
    api.update_status(str(start()))

else:
    for i,content in enumerate(df['TEXT']):
        bracketless = re.search(r"\[([A-Za-z0-9_]+)\]", content)
        if bracketless:
            df.at[i, 'TEXT'] = bracketless.group(1)
    df.to_csv('replies.csv', index=False)  

    guess = df.iat[i,1]
    api.update_status(status = 'thanks', in_reply_to_status_id = df.iat[i,0] , auto_populate_reply_metadata=True)

    if 'guess' not in globals():
        guess = random.choice(guess_list)

    api.update_status(str(main(guess, current_row, not_win, new, correct_word, word_num)))
