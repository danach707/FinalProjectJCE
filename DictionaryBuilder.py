import StringOperations as sc
import Lists
import Enums as e
import threading
import os

class DictionaryBuilder:
    """ DictionaryBuilder class is responsible holding words and numbers lists and build the dictionary according to them."""

    def __init__(self):
        self.lists = Lists.Lists()
        self.default_max_len = 1000
        self.default_min_len = 2
        self.dict_path = './dictionaries/'
        self.fileName = "dictionary.txt"

    def buildDictionary(self, word_min_len, word_max_len, filename, progressbar):
        """ Builds the dictionary according to the length boundary it gets."""

        if not os.path.exists(self.dict_path):
            os.makedirs(self.dict_path)

        global wmax, wmin
        if word_max_len is None or not word_max_len.isdigit():
            wmax = self.default_max_len
        else:
            wmax = int(word_max_len)

        if word_min_len is None or not word_min_len.isdigit():
            wmin = self.default_min_len
        else:
            wmin = int(word_min_len)

        if filename is not None and filename != '':
            self.fileName = filename+'.txt'

        path = self.dict_path + self.fileName
        c = sc.Combinations(self.lists, wmax, wmin, path, progressbar)
        threading.Thread(target=c.combinations).start()

    def clean_lists(self, mode):
        """ Removes duplicates from the lists and make word list values lowercase"""
        if mode == e.Mode_Words:
            tmp = set([v.lower() for v in self.lists.words])
            self.lists.words = list(tmp)
        elif mode == e.Mode_Numbers:
            tmp = set(self.lists.numbers)
            self.lists.numbers = list(tmp)

    def extend_dictionary(self, elist, mode):
        """ Gets a list and a mode and extend the relevant list according to the mode provided."""
        if mode == e.Mode_Words:
            self.lists.words.extend(elist)
        elif mode == e.Mode_Numbers:
            self.lists.numbers.extend(elist)
        self.clean_lists(mode)
