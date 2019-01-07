import StringCombinations as sc
import Lists



class DictionaryBuilder:

    def __init__(self, wordsList, numbersList):
        self.wordList = wordsList
        self.numbersList = numbersList

    def buildDictionary(self):
        mergedList = self.wordList + self.numbersList
        permotatedDict = sc.heapPermutate(list=mergedList, size=len(mergedList), n=len(mergedList))
        print(permotatedDict)


if __name__ == "__main__":
    dictionary = DictionaryBuilder(Lists.words, Lists.numbers)
    list = dictionary.buildDictionary()
    print(list)