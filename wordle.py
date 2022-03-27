import pandas
df2 = pandas.read_csv('counter.csv')
wordle_grid = []


def start(word_num):
    df2.at[0,'CURRENT_ROW'] = 1
    df2.at[0,'WIN'] = 'False'
    df2.to_csv('counter.csv', index=False) 
    
    with open("wordle_grid.txt", "w") as f:
        f.write("")
    
    return("Twitter Plays Wordle #"+str(word_num)+"\n"+"Reply with a valid guess"+"\n"+("\n"+"⬛⬛⬛⬛⬛"+"\n")*6)


def get_wordle_grid():
    with open("wordle_grid.txt", "r") as f:
        for line in f:
            wordle_grid.append(line)


def colour(guess, wordle_grid, correct_word):
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


def main(guess, current_row, wordle_grid, correct_word, word_num):
    wordle_grid.append("   ".join(guess.upper())+"\n")
    colour(guess, wordle_grid, correct_word)
    
    result = ("Twitter Plays Wordle #"+str(word_num)+"\n")
    result += ("Reply with a valid guess"+"\n")
    result += ("\n"+"".join(wordle_grid)+"\n")
    result += ("\n"+"⬛⬛⬛⬛⬛"+"\n")*(6-current_row)
    wordle_grid.append("\n")

    with open("wordle_grid.txt", "w") as f:
        for i in wordle_grid:
            f.write(str(i))

    if guess == correct_word:
        win_message = ["Genius","Magnificent","Impressive","Splendid","Great","Phew"]
        df2.at[0,'WIN'] = 'True'
        df2.at[0, 'WORD_NUM'] += 1
        result = ("Twitter Plays Wordle #"+str(word_num)+"\n")
        result += ("\n"+"".join(wordle_grid)+"\n")
        result += ("\n"+"⬛⬛⬛⬛⬛"+"\n")*(6-current_row)
        result += ("\n"+win_message[current_row-1]+", new word in 30 minutes.")

    if df2.at[0, 'CURRENT_ROW'] == 6 and guess != correct_word:
        result+=("\n"+"The word was \""+correct_word+"\"")
        df2.at[0, 'WORD_NUM'] += 1

    df2.at[0, 'CURRENT_ROW'] += 1
    df2.to_csv('counter.csv', index=False)
    
    return(result)
