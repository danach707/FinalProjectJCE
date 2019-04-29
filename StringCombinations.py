

def combinations(p_list, wordMaxLen, wordMinLen, filename):

    if p_list is None:
        return

    words = [p_list.words, p_list.numbers]
    if len(words[0]) == 0:
        words.pop(0)
    elif len(words[1]) == 0:
        words.pop(1)

    print(words)

    # Words before numbers:
    itr1 = concatenateTwoListsCells(words, wordMaxLen, wordMinLen, filename)
    # itr1 before special characters:
    itr11 = concatenateTwoListsCells([itr1, p_list.spec_characters], wordMaxLen, wordMinLen, filename)
    # special characters before itr1:
    itr12 = concatenateTwoListsCells([p_list.spec_characters, itr1], wordMaxLen, wordMinLen, filename)
    # special characters before itr11:
    concatenateTwoListsCells([p_list.spec_characters, itr11], wordMaxLen, wordMinLen, filename)
    # special characters before itr12:
    concatenateTwoListsCells([p_list.spec_characters, itr12], wordMaxLen, wordMinLen, filename)
    # special characters after itr11:
    concatenateTwoListsCells([itr11, p_list.spec_characters], wordMaxLen, wordMinLen, filename)
    # special characters after itr12:
    concatenateTwoListsCells([itr12, p_list.spec_characters], wordMaxLen, wordMinLen, filename)

def getSpecialCamelCase(word):
    word.lower()


def concatenateTwoListsCells(clist, wordMaxLen, wordMinLen, filename):
    if len(clist) > 2:
        return
    rlist = []
    with open(filename, "a") as dict:
        for clist_index in range(1, len(clist)):
            # 2 lists from clist list.
            curr_list = clist[clist_index]
            before_list = clist[clist_index-1]
            # concatenate each word from before list to current list.
            for index_before_list in range(len(before_list)):
                for index in range(len(curr_list)):
                    newWord = before_list[index_before_list] + curr_list[index]
                    if wordMinLen <= len(newWord) <= wordMaxLen:
                        dict.write(newWord+"\n")
                        rlist.append(newWord)
    return rlist