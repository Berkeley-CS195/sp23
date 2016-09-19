with open('words.txt') as wordfile:
    words = wordfile.read().split('\n')
    def hash(sid):
        first_half = sid // 10000
        return words[first_half] + ' ' + words[(sid % 10000) * first_half % len(words)]
