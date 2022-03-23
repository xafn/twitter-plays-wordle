import tweepy, ssl, pandas, csv, re, random
from wordle import *

guess_list = open('available_words.txt').read().splitlines()

ssl._create_default_https_context = ssl._create_unverified_context

consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#get the most recent tweet's id from the bot's timeline
name = 'WordleGame_Bot'
tweets_list= api.user_timeline(screen_name=name, count=1, exclude_replies=True)
recent_tweet = tweets_list[0]
tweet_id = recent_tweet.id_str

replies=[]
#get 300 tweets of the most recent tweets replying to the bot
for tweet in tweepy.Cursor(api.search_tweets,q='to:'+name, result_type='recent').items(1000):
    #if the replies are replying to the most recent tweet, add tweet to replies list
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        if (tweet.in_reply_to_status_id_str==tweet_id):
            replies.append(tweet)

with open('replies.csv', 'w') as f:
    #create csv of id, text, and likes of each tweet in replies
    csv_writer = csv.DictWriter(f, fieldnames=('ID', 'TEXT', 'LIKES'))
    csv_writer.writeheader()
    for tweet in replies:
        text = tweet.text.replace('@WordleGame_Bot ', '')
        text = text.replace('\n', ' ')
        text = text.lower()
        row = {'ID': tweet.id_str, 'TEXT': text, 'LIKES': tweet.favorite_count}
        if '\[' and ']' in text or len(text) == 5:
            csv_writer.writerow(row)
  
df = pandas.read_csv('replies.csv')
df = df.sort_values('LIKES', ascending=False)
df.to_csv('replies.csv', index=False)  

df2 = pandas.read_csv('counter.csv')

if df2.at[0,'CURRENT_ROW'] == 7 or df2.at[0,'CURRENT_ROW'] == 0 or bool(df2.at[0,'WIN']):
    api.update_status(str(start()))

else:
    #get the text within the FIRST set of square brackets of the tweet (this wont cause any errors if the tweet has no brackets)
    for i,content in enumerate(df['TEXT']):
        bracketless = re.search(r"\[([A-Za-z0-9_]+)\]", content)
        if bracketless:
            df.at[i, 'TEXT'] = bracketless.group(1)
    df.to_csv('replies.csv', index=False)  

    for i,content in enumerate(df['TEXT']):
        if content in guess_list and len(content) == 5:
            guess = df.iat[i,1]
            break

    #if there are no valid replies (lel dead bot), choose a random word from the guess list and use that
    if 'guess' not in locals() and 'guess' not in globals():
        guess = random.choice(guess_list)

    else:
        api.update_status(status = 'thanks', in_reply_to_status_id = df.iat[i,0] , auto_populate_reply_metadata=True)

    api.update_status(str(main(guess, current_row, win, wordle_grid, correct_word, word_num)))
