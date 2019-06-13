import re
import Enums as modes


def combinations(p_list, wordMaxLen, wordMinLen, filename, progressbar):
    """ creates combinations of words based on the Lists objects receives. Adds the words to the dictionary"""

    if p_list is None:
        return

    p_list.words = init_list(p_list.words, wordMaxLen, wordMinLen, filename)
    progressbar.value = 80

    # (1): Words before numbers: (aaa111)
    words_before_numbers = concatenate_two_lists_cells(p_list.words, p_list.numbers, wordMaxLen, wordMinLen, filename)
    progressbar.value = 120

    # (2): numbers with numbers: (111222)
    numbers_with_numbers = concatenate_two_lists_cells(p_list.numbers, p_list.numbers, wordMaxLen, wordMinLen, filename)
    progressbar.value = 300

    # (3): words with words: (aaabbb)
    words_with_words = concatenate_two_lists_cells(p_list.words, p_list.words, wordMaxLen, wordMinLen, filename)
    progressbar.value = 380

    # (4): (3) with numbers: (aaabbb111)
    www_with_numbers = concatenate_two_lists_cells(words_with_words, p_list.numbers, wordMaxLen, wordMinLen, filename)
    progressbar.value = 460

    # (5): (1) before special characters: (aaa111@)
    one_before_spec = concatenate_two_lists_cells(words_before_numbers, p_list.spec_characters, wordMaxLen, wordMinLen, filename)
    progressbar.value = 540

    # (6): (4) with special characters: (aaabbb111@)
    concatenate_two_lists_cells(www_with_numbers, p_list.spec_characters, wordMaxLen, wordMinLen, filename)
    progressbar.value = 660

    # (7): (5) with numbers: (aaa111@111)
    concatenate_two_lists_cells(one_before_spec, p_list.numbers, wordMaxLen, wordMinLen, filename)
    progressbar.value = 740

    # (8): (5) with words: (aaa111@aaa)
    concatenate_two_lists_cells(one_before_spec, p_list.words, wordMaxLen, wordMinLen, filename)
    progressbar.value = 860

    # (9): words with (2): (aaa111222)
    words_with_three = concatenate_two_lists_cells(p_list.words, numbers_with_numbers, wordMaxLen, wordMinLen, filename)
    progressbar.value = 940

    # (10): (9) with special characters: (aaa111222@)
    concatenate_two_lists_cells(words_with_three, p_list.spec_characters, wordMaxLen, wordMinLen, filename)
    progressbar.value = 960

    # (11): (5) with special characters: (aaabbb@)
    concatenate_two_lists_cells(words_with_words, p_list.spec_characters, wordMaxLen, wordMinLen, filename)
    progressbar.value = 1000


def get_special_camel_case(word):
    """ receives a word from the dictionary and returns a list containing the word in lowercase, uppercase, and camel case"""
    words = []

    word = word.upper()
    words.append(word)

    word = word.lower()
    words.append(word)

    # camel case to each letter in the word:
    for i in range(len(word)):
        word = word.lower()
        word = word[:i].lower() + word[i:].capitalize()
        words.append(word)

    return words


def init_list(list, wordMaxLen, wordMinLen, filename):
    rlist = []
    for index in range(len(list)):
        if wordMinLen <= len(list[index]) <= wordMaxLen:
            new_words = get_special_camel_case(list[index])
            rlist.extend(new_words)
        else:
            del list[index]

    list.extend(rlist)
    write_words_to_dictionary(list, filename)
    return list


def concatenate_two_lists_cells(list_before, list_after, wordMaxLen, wordMinLen, filename):
    """ gets two lists and concatenate each cell in the list_before to a cell in the list_after.
        the function returns a list of the concatenated words."""

    rlist = []

    if len(list_before) == 0 or len(list_after) == 0:
        return rlist

    for index_before_list in range(len(list_before)):
        for index_after_list in range(len(list_after)):
            new_word = list_before[index_before_list] + list_after[index_after_list]
            if wordMinLen <= len(new_word) <= wordMaxLen:
                new_words_camel_case = get_special_camel_case(new_word)
                rlist.append(new_word)
                rlist.extend(new_words_camel_case)

    write_words_to_dictionary(rlist, filename)
    return rlist


def write_words_to_dictionary(words, filename):
    """ writes a list of words to the filename specified"""
    with open(filename, "a") as dict:
        for word in words:
            dict.write(word + "\n")


def parse_email(email, mode):
    """ gets an email in the format example@email.com and parse the words and return words if the mode is Mode_words
        and numbers if the mode is Mode_numbers. """
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


def parse_dob(dob):
    """ gets a birthday date in the format XX/XX/XXXX (or other separators) and return the numbers separated,
    the string without separators and adds 0 if the number is less than 10"""
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

    if changed > 0:
        res.append(''.join(nums))
    return res



def clean_data(data):
    """ gets the data and returns a list of the words to the dictionary."""
    # delete new lines and spaces:
    data = data.strip()
    data = re.split(r"\n| |,", data)
    # filter none relevant elements:
    regex = re.compile(r'^[\w]+[A-Za-z0-9|\W]*[\w]+$')
    data = list(filter(regex.search, data))
    print("in clean result:", data)
    return data


def split_by_separator(data):
    """ gets a data divided by separators that are not words characters
    and returns a list of the words separated"""
    return re.compile(r'\W+').split(data)

