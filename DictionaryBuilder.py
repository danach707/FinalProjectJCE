import StringCombinations as sc
import Lists

class DictionaryBuilder:

    def __init__(self, wordMaxLen = 1000, wordMinLen = 2):
        self.lists = Lists.Lists()
        self.wordMaxLen = wordMaxLen
        self.wordMinLen = wordMinLen
        self.fileName = "dictionary.txt"

    def buildDictionary(self):
        sc.combinations(self.lists, self.wordMaxLen, self.wordMinLen, self.fileName)
