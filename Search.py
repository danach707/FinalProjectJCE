import sys
import Enums as errors
from pathlib import Path
import threading

class Search:

    def __init__(self, word, file, progressbar):
        self.similar_pass = ""
        self.min_mistakes = 0
        self.word = word
        self.file = file
        self.progressbar = progressbar
        self.res = ''

    def search(self):
        self.progressbar(0)
        if self.word is None:
            self.similar_pass = ""
            self.res = errors.Error_Empty_Password
            self.progressbar(1)
            return

        if self.file == '' or not Path(self.file).is_file():
            self.similar_pass = ""
            self.res = errors.Error_No_Dictionary
            self.progressbar(1)
            return

        min_mistakes = sys.maxsize
        with open(self.file, 'r') as f:
            for wordFromFile in f.readlines():
                wordFromFile = wordFromFile.rstrip()

                if wordFromFile == self.word:
                    self.similar_pass = wordFromFile
                    self.min_mistakes = 0
                    self.res = errors.Password_Found
                    self.progressbar(1)
                    return

                if len(wordFromFile) == len(self.word):
                    mistakes = self.count_mistakes(wordFromFile, self.word)
                    if min_mistakes > mistakes:
                        min_mistakes = mistakes
                        self.similar_pass = wordFromFile
                self.progressbar(0)

        if min_mistakes != sys.maxsize and min_mistakes != len(self.word):
            self.min_mistakes = min_mistakes
            self.res = errors.Password_Found
            self.progressbar(1)
            return
        else:
            self.res = errors.Password_Not_Found
            self.progressbar(1)
            return


    def count_mistakes(self, word1, word2):
        mistakes = 0
        for index in range(len(word1)):
            if word1[index] != word2[index]:
                mistakes = mistakes + 1
        return mistakes

    def normalize_input(self, word):
        return self.getchars(word.lower())

    def getchars(self, word):
        chars = ''
        for char in word:
            if char.isalpha():
                chars += char
        return chars

    def calculate_mistakes_percentage(self, password):
        """Calculate how close was the password entered to a password in the dictionary in percentages.
        return an identical percentage
        """
        return 100 - ((self.min_mistakes/len(password))*100)
