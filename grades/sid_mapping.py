wordfile = open('words.txt')
words = wordfile.read().split('\n')

import random
random.seed('JoshDanielHugFeldman2016') # Random seed don't tell people this
random.shuffle(words)

def get_sid_name(sid):
    codewords = []

    first_word = sid % 1000
    sid = sid // 1000

    second_word = sid % 1000
    sid = sid // 1000

    third_word = sid % 1000
    third_word_reverse = int(str(third_word)[::-1])


    return " ".join([words[codeword] for codeword in [first_word, second_word, third_word_reverse]])

