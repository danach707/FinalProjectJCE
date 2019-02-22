import StringCombinations as sc


class DictionaryBuilder:

    def __init__(self, wordMaxLen = 1000, wordMinLen = 2):
        self.wordList = []
        self.numbersList = []
        self.wordMaxLen = wordMaxLen
        self.wordMinLen = wordMinLen
        self.fileName = "dictionary.txt"

    def buildDictionary(self):
        sc.combinations([self.wordList, self.numbersList], self.wordMaxLen, self.wordMinLen, self.fileName)

    def cleanLists(self):
        self.wordList.clear()
        self.numbersList.clear()

