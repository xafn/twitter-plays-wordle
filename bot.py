import time
import pandas
import random
import os
import credentials as crds
import replies
import wordle

guess_list = open('available_words.txt').read().splitlines()
clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def run():
    while True:
        df2 = pandas.read_csv('counter.csv')
        current_row = df2.iat[0,0]
        word_num = df2.iat[0,1]
        win = bool(df2.iat[0,2])
        correct_word = (open('words_list.txt').read().splitlines())[word_num-1]

        if current_row == 7 or current_row == 0 or win:
            crds.api.update_status(wordle.start(word_num))
            clear()
            print(f'Posted blank word grid #{word_num}')

        else:
            try:
                guess, guess_id = replies.get_guess(guess_list)
                crds.api.update_status(status = 'thanks', in_reply_to_status_id = guess_id, auto_populate_reply_metadata=True)
            except Exception:
                guess = random.choice(guess_list)
            
            crds.api.update_status(wordle.main(guess, current_row, wordle.wordle_grid, correct_word, word_num))
            clear()
            print(f'Posted word #{word_num} at row {current_row}')

        time.sleep(1800)

if __name__ == "__main__":
    run()
