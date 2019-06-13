
def printto_lbllist(words, lbl_list):

    if words is None:
        lbl_list.text = 'No Words in the list'
        return

    lbl_list.text = ''
    if type(words) is list:
        for w in words:
            lbl_list.text += "%s\n" % w
    else:
        lbl_list.text += "%s\n" % words