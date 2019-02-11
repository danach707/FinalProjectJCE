import DictionaryBuilder as db
import Lists
import Search
import Questionirre as quest

if __name__ == "__main__":
    dictionary = db.DictionaryBuilder(Lists.words, Lists.numbers, 1000, 6)
    dict = dictionary.buildDictionary()

    word_list = quest.words_questions()
    numbers_list = quest.numbers_questions()

    password = input('password: ')
    result = Search.search(password, dictionary.fileName)
    mistakes = result[0]
    passFromDict = result[1]
    if mistakes == 0:
        print('Your password found in the dictionary!')
    elif mistakes > 0:
        print('Your password found in the dictionary, but with %d mistakes.\nRelated password is: %s' % (mistakes, passFromDict))
    else:
        print('Your password did not found in the dictionary.')

