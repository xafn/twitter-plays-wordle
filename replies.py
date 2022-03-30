import csv, pandas, tweepy, re
import credentials as crds


def get_recent_tweet_id():
    name = 'WordleGame_Bot'
    tweets_list= crds.api.user_timeline(screen_name=name, count=1, exclude_replies=True)
    recent_tweet = tweets_list[0]
    tweet_id = recent_tweet.id_str

    return tweet_id, name


def get_replies():
    tweet_id, name = get_recent_tweet_id()
    replies = []

    for tweet in tweepy.Cursor(crds.api.search_tweets,q='to:'+name, result_type='recent').items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet)

    return replies


def filter_guesses_from_replies():
    replies = get_replies()
    with open('replies.csv', 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=('ID', 'TEXT', 'LIKES'))
        csv_writer.writeheader()

        for tweet in replies:
            text = tweet.text.replace('@WordleGame_Bot ', '')
            text = text.replace('\n', ' ')
            text = text.replace(',' ,  '')
            text = text.lower()
            row = {'ID': tweet.id_str, 'TEXT': text, 'LIKES': tweet.favorite_count}
            if '\[' and ']' in text or len(text) == 5:
                csv_writer.writerow(row)


def read_csv_as_dataframe():
    return pandas.read_csv('replies.csv', encoding= 'unicode_escape')


def remove_brackets():
    df = read_csv_as_dataframe()
    for i,content in enumerate(df['TEXT']):
        if "\[" and "]" in content:
            bracketless = re.search(r"\[([A-Za-z0-9_]+)\]", content).group(1)
            df.at[i,'TEXT'] = bracketless
    df.to_csv('replies.csv', index=False)


def sort_by_likes():
    df = read_csv_as_dataframe()
    df = df.sort_values('LIKES', ascending=False)
    df.to_csv('replies.csv', index=False)


def get_guess(guess_list):
    filter_guesses_from_replies()
    remove_brackets()
    sort_by_likes()
    df = read_csv_as_dataframe()
    for i,content in enumerate(df['TEXT']):
        if content in guess_list and len(content) == 5:
            guess = df.iat[i,1]
            guess_id = df.iat[i,0]
            break

    return guess, guess_id
