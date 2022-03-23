import pandas, os
clear = lambda: os.system('clear')

df2 = pandas.read_csv('counter.csv')
current_row = df2.iat[0,0]
word_num = df2.iat[0,1]
win = bool(df2.iat[0,2])
guess_list = open('available_words.txt').read().splitlines()
correct_word = (open('words_list.txt').read().splitlines())[word_num-1]
row = "⬛⬛⬛⬛⬛"
wordle_grid = []

#add whatevers in wordle_grid.txt to wordle_grid variable as a list
with open("wordle_grid.txt", "r") as f:
  for line in f:
    wordle_grid.append(line)

def start():
    #clear everything, return blank grid
    clear()
    df2.at[0,'CURRENT_ROW'] = 1
    df2.at[0,'WIN'] = 'False'
    df2.to_csv('counter.csv', index=False) 
    with open("wordle_grid.txt", "w") as f:
        f.write("")
    return("Twitter Plays Wordle #"+str(word_num)+"\n"+"Reply with a guess in square brackets [ ]"+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*6)

def colour(guess, wordle_grid):
    #run wordle colour algorithm, add all results as list to wordle_grid variable
    for i,char in enumerate(guess):
        if correct_word[i] == guess[i]:
            wordle_grid.append("🟩")

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
                wordle_grid.append("🟨")
                
            else:
                wordle_grid.append("⬜")

        else:
            wordle_grid.append("⬜")

def main(guess, current_row, win, wordle_grid, correct_word, word_num):

    if df2.at[0,'CURRENT_ROW'] == 6 and df2.at[0,'WIN'] == bool(True):
        wordle_grid = []
        with open("wordle_grid.txt", "w") as f:
            f.write(str(wordle_grid))
        df2.at[0,'CURRENT_ROW'] = 0 
        df2.at[0,'WORD_NUM'] += 1
        df2.at[0,'WIN'] = 'False'
        df2.to_csv('counter.csv', index=False) 

    while current_row < 7 and not win:
        #add the guess to the wordle_grid list (spaced out by 3 for twitter) and then run colour algorithm
        wordle_grid.append("   ".join(guess.upper())+"\n")
        colour(guess, wordle_grid)
        clear()
        result = ("Twitter Plays Wordle #"+str(word_num)+"\n"+"Reply with a guess in square brackets [ ]"+"\n\n"+"".join(wordle_grid)+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*(6-current_row))
        wordle_grid.append("\n")
        with open("wordle_grid.txt", "w") as f:
            for i in wordle_grid:
                f.write(str(i))

        if guess == correct_word:
            #change variables in the counter.csv, and add the corresponding win message to the result
            win_message = ["Genius","Magnificent","Impressive","Splendid","Great","Phew"]
            df2.at[0,'WIN'] = 'True'
            df2.at[0, 'WORD_NUM'] += 1
            result = ("Twitter Plays Wordle #"+str(word_num)+"\n\n"+"".join(wordle_grid)+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*(6-current_row))
            result+=("\n"+win_message[current_row-1]+", new word in 30 minutes.")

        if df2.at[0, 'CURRENT_ROW'] == 6 and guess != correct_word:
            #add the lose message to the result
            result+=("\n"+"The word was \""+correct_word+"\"")
            df2.at[0, 'WORD_NUM'] += 1

        df2.at[0, 'CURRENT_ROW'] += 1
        df2.to_csv('counter.csv', index=False)
        return(result)
