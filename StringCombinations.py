
def combinations(p_list):
    # connect cells in the list
    concatList = concatenateCells(p_list)
    return concatList


def concatenateCells(clist):
    rlist = []
    index_before_list = 0
    for clist_index in range(1, len(clist)):
        # 2 lists from clist list.
        curr_list = clist[clist_index]
        before_list = clist[clist_index-1]

        # concatenate each word from before list to current list.
        for index_before_list in range(len(before_list)):
            for index in range(len(curr_list)):
                rlist.append(before_list[index_before_list] + curr_list[index])
    return rlist