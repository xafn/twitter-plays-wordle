import time, pandas, random, os
import credentials as crds
import replies
import wordle

guess_list = open('available_words.txt').read().splitlines()
clear = lambda: os.system('clear')

if __name__ == "__main__":
    while True:
        df2 = pandas.read_csv('counter.csv')
        current_row = df2.iat[0,0]
        word_num = df2.iat[0,1]
        win = bool(df2.iat[0,2])
        correct_word = (open('words_list.txt').read().splitlines())[word_num-1]
        wordle.wordle_grid = []

        if df2.at[0,'CURRENT_ROW'] == 7 or df2.at[0,'CURRENT_ROW'] == 0 or bool(df2.at[0,'WIN']):
            crds.api.update_status(wordle.start(word_num))
            clear()
            print('done')

        else:
            try:
                guess, guess_id = replies.get_guess(guess_list)
                crds.api.update_status(status = 'thanks', in_reply_to_status_id = guess_id, auto_populate_reply_metadata=True)
            except:
                guess = random.choice(guess_list)
            
            wordle.get_wordle_grid()    
            crds.api.update_status(wordle.main(guess, current_row, wordle.wordle_grid, correct_word, word_num))
            clear()
            print('done')

        time.sleep(1800)
