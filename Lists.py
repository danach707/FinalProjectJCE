
class Lists:

    def __init__(self):
        self.words = []
        self.numbers = []
        self.spec_characters = [chr(x) for x in range(33, 65)] + [chr(x) for x in range(91, 97)]

    def cleanLists(self):
        self.words.clear()
        self.numbers.clear()