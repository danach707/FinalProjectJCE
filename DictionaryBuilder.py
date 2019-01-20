import StringCombinations as sc
import Lists


class DictionaryBuilder:

    def __init__(self, wordsList, numbersList, wordMaxLen = 1000, wordMinLen = 2):
        self.wordList = wordsList
        self.numbersList = numbersList
        self.wordMaxLen = wordMaxLen
        self.wordMinLen = wordMinLen


    def buildDictionary(self):
        permotatedDict = sc.combinations([self.wordList, self.numbersList], self.wordMaxLen, self.wordMinLen)
        print("from DB: ", permotatedDict)
        return permotatedDict


if __name__ == "__main__":
    dictionary = DictionaryBuilder(Lists.words, Lists.numbers, 1000, 6)
    dictionary.buildDictionary()

    with open("dictionary.txt", "r") as dict:
        print(dict.read())
