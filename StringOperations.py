import re
import Enums as modes


""" creates combinations of words based on the Lists objects receives. Adds the words to the dictionary"""
def combinations(p_list, wordMaxLen, wordMinLen, filename):

    if p_list is None:
        return

    # (1): Words before numbers: (aaa111)
    words_before_numbers = concatenate_two_lists_cells(p_list.words, p_list.numbers, wordMaxLen, wordMinLen, filename)

    # (2): Numbers before words: (111aaa)
    numbers_before_words = concatenate_two_lists_cells(p_list.numbers, p_list.words, wordMaxLen, wordMinLen, filename)

    # (3): numbers with numbers: (111222)
    numbers_with_numbers = concatenate_two_lists_cells(p_list.numbers, p_list.numbers, wordMaxLen, wordMinLen, filename)

    # (4): words with words: (aaabbb)
    words_with_words = concatenate_two_lists_cells(p_list.words, p_list.words, wordMaxLen, wordMinLen, filename)

    # (5): (4) with numbers: (aaabbb111)
    www_with_numbers = concatenate_two_lists_cells(words_with_words, p_list.numbers, wordMaxLen, wordMinLen, filename)

    # (6): (1) before special characters: (aaa111@)
    one_before_spec = concatenate_two_lists_cells(words_before_numbers, p_list.spec_characters, wordMaxLen, wordMinLen, filename)

    # (7): (5) with special characters: (aaabbb111@)
    five_before_spec = concatenate_two_lists_cells(www_with_numbers, p_list.spec_characters, wordMaxLen, wordMinLen, filename)

    # (8): (6) with numbers: (aaa111@111)
    six_with_numbers = concatenate_two_lists_cells(one_before_spec, p_list.numbers, wordMaxLen, wordMinLen, filename)

    # (9): (6) with words: (aaa111@aaa)
    six_with_words = concatenate_two_lists_cells(one_before_spec, p_list.words, wordMaxLen, wordMinLen, filename)

    # (10): words with (3): (aaa111222)
    words_with_three = concatenate_two_lists_cells(p_list.words, numbers_with_numbers, wordMaxLen, wordMinLen, filename)

    # (11): (10) with special characters: (aaa111222@)
    ten_with_spec = concatenate_two_lists_cells(words_with_three, p_list.spec_characters, wordMaxLen, wordMinLen, filename)

    # (12): (5) with special characters: (aaabbb@)
    www_with_spec = concatenate_two_lists_cells(words_with_words, p_list.spec_characters, wordMaxLen, wordMinLen, filename)

    # (13): (3) with special characters: (111222@)
    nwn_with_spec = concatenate_two_lists_cells(numbers_with_numbers, p_list.spec_characters, wordMaxLen, wordMinLen, filename)


def get_special_camel_case(word):
    word.lower()


""" gets two lists and concatenate each cell in the list_before to a cell in the list_after.
    the function returns a list of the concatenated words."""
def concatenate_two_lists_cells(list_before, list_after, wordMaxLen, wordMinLen, filename):

    rlist = []

    if len(list_before) == 0 or len(list_after) == 0:
        return rlist

    for index_before_list in range(len(list_before)):
        for index_after_list in range(len(list_after)):
            new_word = list_before[index_before_list] + list_after[index_after_list]
            if wordMinLen <= len(new_word) <= wordMaxLen:
                rlist.append(new_word)

    write_words_to_dictionary(rlist, filename)
    return rlist


""" writes a list of words to the filename specified"""
def write_words_to_dictionary(words, filename):
    with open(filename, "a") as dict:
        for word in words:
            dict.write(word + "\n")


""" gets an email in the format example@email.com and parse the words and return words if the mode is Mode_words
    and numbers if the mode is Mode_numbers. """
def parse_email(email, mode):
    prefix = email.split("@")[0]
    regex = ''
    if mode == modes.Mode_Words:
        regex = r'([a-zA-Z]+)'
    elif mode == modes.Mode_Numbers:
        regex = r'([0-9]+)'
    res = []

    match = re.findall(regex, prefix)
    for i in match:
        res.append(i)
    return res


""" gets a birthday date in the format XX/XX/XXXX (or other separators) and return the numbers separated,
the string without separators and adds 0 if the number is less than 10"""
def parse_dob(dob):
    res = []

    # numbers without zero's
    nums = split_by_separator(dob)
    res.extend(nums)
    res.append(''.join(nums))
    changed = 0

    for i, num in enumerate(nums):
        if num.isdigit() and num[0] != '0' and int(num) < 10:
            nums[i] = '%s%s' % (str(0), num)
            res.append(nums[i])
            changed = 1
            print(changed)

    print(changed)
    if changed > 0:
        print("changes")
        res.append(''.join(nums))
    return res


""" gets the data and returns a list of the words to the dictionary."""
def clean_data(data):
    # delete new lines and spaces:
    data = data.strip()
    data = re.split(r"\n| |,", data)
    # filter none relevant elements:
    regex = re.compile(r'^[\w]+[A-Za-z0-9|\W]*[\w]+$')
    data = list(filter(regex.search, data))
    print("in clean result:", data)
    return data


""" gets a data divided by separators that are not words characters
and returns a list of the words separated"""
def split_by_separator(data):
    return re.compile(r'\W+').split(data)

