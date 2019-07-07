import Enums as e
from pathlib import Path
from itertools import islice
import ahocorasick
from collections import Counter
import sys


class Search:
    """ Search class provide a search engine for the user to search his password and get the best match from the dictionary."""

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
        """ search methos, gets a word and fine the best match in the dictionary """

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

        self.min_mistakes = sys.maxsize
        A = ahocorasick.Automaton()
        already_read = 0
        similar_passwords = list()
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

                if distance == self.min_mistakes and distance != len(self.word):
                    similar_passwords.append(key)
                elif distance < self.min_mistakes:
                    self.min_mistakes = distance
                    similar_passwords.clear()
                    similar_passwords.append(key)

                already_read += self.__buffer_size

        if self.min_mistakes < len(self.word):
            self.similar_pass = self.get_best_match(similar_passwords)
            self.res = e.Password_Found
            self.progressbar(e.Finish_Progress)
        else:
            self.res = e.Password_Not_Found
            self.progressbar(e.Finish_Progress)
        print('finished')

    def get_best_match(self, similar_passwords):
        """ returns the best match from a given list of passwords"""
        if len(similar_passwords) == 0:
            return e.Password_Not_Found
        print(similar_passwords)

        min_mistakes = sys.maxsize
        similar_pass = similar_passwords[0]

        for password in similar_passwords:
            mistakes = self.count_mistakes(self.word, password)
            if mistakes < min_mistakes:
                min_mistakes = mistakes
                similar_pass = password
        return similar_pass

    def count_mistakes(self, word1, word2):
        """ counts the different characters between word1 and word2"""
        mistakes = 0
        if len(word1) > len(word2):
            lenw = len(word2)
        else:
            lenw = len(word1)
        mistakes += len(word1) - len(word2)

        for index in range(lenw):
            if word1[index] != word2[index]:
                mistakes = mistakes + 1
        return mistakes

    def normalize_input(self, word):
        return self.getchars(word.lower())

    def getchars(self, word):
        """ return the numbers of alpha chars in a given string"""
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
