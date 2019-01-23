import StringCombinations as sc


class DictionaryBuilder:

    def __init__(self, wordsList, numbersList, wordMaxLen = 1000, wordMinLen = 2):
        self.wordList = wordsList
        self.numbersList = numbersList
        self.wordMaxLen = wordMaxLen
        self.wordMinLen = wordMinLen
        self.fileName = "dictionary.txt"

    def buildDictionary(self):
        sc.combinations([self.wordList, self.numbersList], self.wordMaxLen, self.wordMinLen, self.fileName)
        return self.fileName


