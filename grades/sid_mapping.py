wordfile = open('words.txt')
words = wordfile.read().split('\n')

import random
random.seed('JoshDanielHugFeldman2016') # Random seed don't tell people this
random.shuffle(words)

def get_sid_name(sid):
    codewords = []
    
    first_word = sid // 10000

    if first_word > 10000-1:
        first_word = first_word % 10000
        second_word = first_word // 10000
        codewords.append(words[first_word])
        codewords.append(words[second_word])
    else:
        codewords.append(words[first_word])


    
    last_half = sid % 10000
    last_half_reversed = int(str(last_half)[::-1])
    
    codewords.append(words[last_half_reversed])

    return " ".join(codewords)