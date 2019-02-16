import sys
import Enums as matches
from pathlib import Path


class Search:

    def __init__(self):
        self.match = matches.NO_MATCH
        self.similar_pass = ""
        self.min_mistakes = 0

    def search(self, word, file):
        if word is None:
            self.match = matches.ERROR
            self.similar_pass = ""
            return

        if not Path(file).is_file():
            self.match = matches.ERROR
            self.similar_pass = ""
            return

        min_mistakes = sys.maxsize
        with open(file, 'r') as f:
            for wordFromFile in f.readlines():
                wordFromFile = wordFromFile.rstrip()

                if wordFromFile == word:
                    self.match = matches.MATCH
                    self.similar_pass = wordFromFile
                    return

                if len(wordFromFile) == len(word) and self.getchars(wordFromFile.lower()) == self.getchars(word.lower()):
                    mistakes = self.countMistakes(wordFromFile, word)
                    if min_mistakes > mistakes:
                        min_mistakes = mistakes
                        self.similar_pass = wordFromFile

        if min_mistakes != sys.maxsize:
            self.min_mistakes = min_mistakes
            self.match = matches.MATCH
        else:
            self.match = matches.NO_MATCH

    def countMistakes(self, word1, word2):
        mistakes = 0
        for index in range(len(word1)):
            if word1[index] != word2[index]:
                mistakes = mistakes + 1
        return mistakes

    def getchars(self, word):
        chars = ''
        for char in word:
            if char.isalpha():
                chars += char
        return chars