import StringOperations as sc
import Lists
import Enums as e

""" DictionaryBuilder class is responsible holding words and numbers lists and build the dictionary according to them."""
class DictionaryBuilder:

    def __init__(self):
        self.lists = Lists.Lists()
        self.default_max_len = 1000
        self.default_min_len = 2
        self.fileName = "dictionary.txt"

    """ Builds the dictionary according to the length boundary it gets."""
    def buildDictionary(self, word_min_len, word_max_len, filename, progressbar):

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
        sc.combinations(self.lists, wmax, wmin, self.fileName, progressbar)

    """ Removes duplicates from the lists and make word list values lowercase"""
    def clean_lists(self, mode):
        if mode == e.Mode_Words:
            tmp = set([v.lower() for v in self.lists.words])
            self.lists.words = list(tmp)
        elif mode == e.Mode_Numbers:
            tmp = set(self.lists.numbers)
            self.lists.numbers = list(tmp)

    """ Gets a list and a mode and extend the relevant list according to the mode provided."""
    def extend_dictionary(self, elist, mode):
        if mode == e.Mode_Words:
            self.lists.words.extend(elist)
        elif mode == e.Mode_Numbers:
            self.lists.numbers.extend(elist)
        self.clean_lists(mode)
