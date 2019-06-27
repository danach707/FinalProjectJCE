import Enums as e
from pathlib import Path
from itertools import islice
import ahocorasick
from collections import Counter


class Search:

    def __init__(self, word, file, progressbar, num_lines_in_file):
        self.similar_pass = ""
        self.min_mistakes = 0
        self.word = word
        self.file = file
        self.progressbar = progressbar
        self.res = ''
        self.__buffer_size = 131072
        self.num_lines_in_file = num_lines_in_file

    def search(self):
        self.progressbar(0)
        if self.word is None:
            self.similar_pass = ""
            self.res = e.Error_Empty_Password
            self.progressbar(e.Finish_Progress)
            return

        if self.file == '' or not Path(self.file).is_file():
            self.similar_pass = ""
            self.res = e.Error_No_Dictionary
            self.progressbar(e.Finish_Progress)
            return

        self.min_mistakes = len(self.word)
        A = ahocorasick.Automaton()
        already_read = 0

        print(self.num_lines_in_file)
        with open(self.file, 'r') as f:

            while already_read < self.num_lines_in_file:
                buffer = list(islice(f, self.__buffer_size))

                for idx, key in enumerate(buffer):
                    key = key.rstrip()
                    A.add_word(key, (idx, key))

                self.progressbar(self.__buffer_size)
                if self.word in A:
                    self.similar_pass = self.word
                    self.min_mistakes = 0
                    self.res = e.Password_Found
                    self.progressbar(e.Finish_Progress)
                    return

                # check closeness to word:
                word_close_val = Counter(self.word) - Counter(key)
                distance = sum(word_close_val.values())
                if distance < self.min_mistakes:
                    self.min_mistakes = distance
                    self.similar_pass = key

                already_read += self.__buffer_size

        if self.min_mistakes < len(self.word):
            self.res = e.Password_Found
            self.progressbar(e.Finish_Progress)
        else:
            self.res = e.Password_Not_Found
            self.progressbar(e.Finish_Progress)
        print('finished')

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
