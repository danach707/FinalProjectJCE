import sys
import EnumMatches as matches


def search(word, file):

    min_mistakes = sys.maxsize
    similar_pass = ''
    with open(file, 'r') as f:
        for wordFromFile in f.readlines():
            wordFromFile = wordFromFile.rstrip()
            if wordFromFile == word:
                return matches.MATCH, wordFromFile
            if len(wordFromFile) == len(word) and getchars(wordFromFile.lower()) == getchars(word.lower()):
                mistakes = countMistakes(wordFromFile, word)
                if min_mistakes > mistakes:
                    min_mistakes = mistakes
                    similar_pass = wordFromFile

    if min_mistakes != sys.maxsize:
        return min_mistakes, similar_pass
    return matches.NO_MATCH, similar_pass


def countMistakes(word1, word2):
    mistakes = 0
    for index in range(len(word1)):
        if word1[index] != word2[index]:
            mistakes = mistakes + 1
    return mistakes


def getchars(word):
    chars = ''
    for char in word:
        if char.isalpha():
            chars += char
    return chars