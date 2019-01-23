import sys
import EnumMatches as matches


def search(word, file):

    min_mistakes = sys.maxsize
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            if line == word:
                return matches.MATCH
            if len(line) == len(word) and getchars(line.lower()) == getchars(word.lower()):
                mistakes = countMistakes(line)
                if min_mistakes > mistakes:
                    min_mistakes = mistakes
                    print(line)

    if min_mistakes != sys.maxsize:
        return min_mistakes
    return matches.NO_MATCH


def countMistakes(word):
    word_lower = word.lower()
    mistakes = 0
    for index in range(0, len(word)):
        if word[index] != word_lower[index]:
            print(word[index], word_lower[index])
            mistakes += 1
    return mistakes


def getchars(word):
    chars = ''
    for char in word:
        if char.isalpha():
            chars += char
    return chars