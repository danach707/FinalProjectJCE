import StringCombinations as sc
import Lists


class DictionaryBuilder:

    def __init__(self, wordsList, numbersList):
        self.wordList = wordsList
        self.numbersList = numbersList

    def buildDictionary(self):
        permotatedDict = sc.combinations([self.wordList, self.numbersList])
        print("from DB: ", permotatedDict)
        return permotatedDict


if __name__ == "__main__":
    dictionary = DictionaryBuilder(Lists.words, Lists.numbers)
    list = dictionary.buildDictionary()
