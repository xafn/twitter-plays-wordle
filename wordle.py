import pandas, os
clear = lambda: os.system('clear')

guess_list = open('avawords.txt').read().splitlines()
df2 = pandas.read_csv('counter.csv')
not_win = bool(df2.iat[0,2])
current_row = df2.iat[0,0]
word_num = df2.iat[0,1]
new = []

with open("wordleresults.txt", "r") as f:
  for line in f:
    new.append(line)

counter = word_num
correct_word = (open('wordslist.txt').read().splitlines())[word_num-1]

row = "⬛⬛⬛⬛⬛"

def start(current_row):
    clear()
    df2.at[0,'CURRENT_ROW'] = 1
    df2.at[0,'NOT_WIN'] = 'True'
    with open("wordleresults.txt", "w") as f:
        f.write("")
    df2.to_csv('counter.csv', index=False) 
    return("Twitter Plays Wordle #"+str(word_num)+"\n"+"Reply with a guess in [ ]"+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*6)

def colour(guess, new):
    for i,char in enumerate(guess):
        if correct_word[i] == guess[i]:
            new.append("🟩")

        elif char in correct_word:
            target = correct_word.count(char)
            correct = 0
            occur = 0

            for j in range(5):
                if guess[i] == guess[j]:
                    if j <= i:
                        occur += 1
                    if guess[i] == correct_word[j]:
                        correct += 1

            if target - correct - occur >= 0:
                new.append("🟨")
                
            else:
                new.append("⬜")

        else:
            new.append("⬜")

def main(guess, current_row, not_win, new, correct_word, word_num):

    if df2.at[0,'CURRENT_ROW'] == 6 and df2.at[0,'NOT_WIN'] == bool(False):
        new = []
        with open("wordleresults.txt", "w") as f:
            f.write(str(new))
        df2.at[0,'CURRENT_ROW'] = 0 
        df2.at[0,'WORD_NUM'] += 1
        df2.at[0,'NOT_WIN'] = 'True'
        df2.to_csv('counter.csv', index=False) 

    while current_row < 7 and not_win:

        if len(guess) == 5 and guess in guess_list:
            new.append("   ".join(guess.upper())+"\n")
            colour(guess, new)
            clear()
            result = ("Twitter Plays Wordle #"+str(word_num)+"\n"+"Reply with a guess in [ ]"+"\n\n"+"".join(new)+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*(6-current_row)) #heh sorry
            new.append("\n")
            with open("wordleresults.txt", "w") as f:
               for i in new:
                    f.write(str(i))

            if guess == correct_word:
                win_message = ["Genius","Magnificent","Impressive","Splendid","Great","Phew"]
                df2.at[0,'NOT_WIN'] = 'False'
                df2.at[0, 'WORD_NUM'] += 1
                result = ("Twitter Plays Wordle #"+str(word_num)+"\n\n"+"".join(new)+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*(6-current_row)) #heh sorry
                result+=("\n"+win_message[current_row-1]+", new word in 30 minutes.")

            if df2.at[0, 'CURRENT_ROW'] == 6 and guess != correct_word:
                result+=("\n"+"The word was \""+correct_word+"\"")
                df2.at[0, 'WORD_NUM'] += 1

            df2.at[0, 'CURRENT_ROW'] += 1
            df2.to_csv('counter.csv', index=False)
            return(result)