import DictionaryBuilder as db
import Lists
import Search

if __name__ == "__main__":
    dictionary = db.DictionaryBuilder(Lists.words, Lists.numbers, 1000, 6)
    #dict = dictionary.buildDictionary()

    password = input('password: ')
    result = Search.search(password, "dictionary.txt")
    mistakes = result[0]
    passFromDict = result[1]
    if mistakes == 0:
        print('Your password found in the dictionary!')
    elif mistakes > 0:
        print('Your password found in the dictionary, but with %d mistakes.\nRelated password is: %s' % (mistakes, passFromDict))
    else:
        print('Your password did not found in the dictionary.')

