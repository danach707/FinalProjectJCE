
class Lists:

    def __init__(self):
        self.words = []
        self.numbers = []
        self.spec_characters = [chr(x) for x in range(32, 65)] + [chr(x) for x in range(91, 97)]
