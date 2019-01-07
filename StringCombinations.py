

def heapPermutate(list, size, n):

    if size <= 1:
        return list

    for i in range(0, size):
        heapPermutate(list, size-1, n)

        if size % 2 == 1:
            list[0], list[1] = list[1], list[0]

        else:
            list[i], list[size-1] = list[i], list[size-1]

