import Lists

def combinations(p_list, wordMaxLen, wordMinLen):
    # Words before numbers:
    itr1 = concatenateTwoListsCells(p_list, wordMaxLen, wordMinLen)
    # itr1 before special characters:
    itr11 = concatenateTwoListsCells([itr1, Lists.spec_characters], wordMaxLen, wordMinLen)
    # special characters before itr1:
    itr12 = concatenateTwoListsCells([Lists.spec_characters, itr1], wordMaxLen, wordMinLen)
    # special characters before itr11:
    itr21 = concatenateTwoListsCells([Lists.spec_characters, itr11], wordMaxLen, wordMinLen)
    # special characters before itr12:
    itr22 = concatenateTwoListsCells([Lists.spec_characters, itr12], wordMaxLen, wordMinLen)
    # special characters after itr11:
    itr211 = concatenateTwoListsCells([itr11, Lists.spec_characters], wordMaxLen, wordMinLen)
    # special characters after itr12:
    itr222 = concatenateTwoListsCells([itr12, Lists.spec_characters], wordMaxLen, wordMinLen)

def getSpecialCamelCase(word):
    word.lower()



def concatenateTwoListsCells(clist, wordMaxLen, wordMinLen):
    if len(clist) > 2:
        return
    rlist = []
    with open("dictionary.txt", "a") as dict:
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