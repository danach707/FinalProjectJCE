import re
import Enums as modes
import zipfile

class Combinations:
    def __init__(self, p_list, wordMaxLen, wordMinLen, filename, progressbar):
        self.p_list = p_list
        self.wordMaxLen = wordMaxLen
        self.wordMinLen = wordMinLen
        self.filename = filename
        self.progressbar = progressbar
        
    def combinations(self):
        """ Creates combinations of words based on the Lists objects receives. Adds the words to the dictionary """
    
        if self.p_list is None:
            return
    
        self.p_list.words = self.init_list(self.p_list.words)
        self.progressbar()
    
        # (1): Words before numbers: (aaa111)
        words_before_numbers = self.concatenate_two_lists_cells(self.p_list.words, self.p_list.numbers)
        self.progressbar()
    
        # (2): numbers with numbers: (111222)
        numbers_with_numbers = self.concatenate_two_lists_cells(self.p_list.numbers, self.p_list.numbers)
        self.progressbar()
    
        # (3): words with words: (aaabbb)
        words_with_words = self.concatenate_two_lists_cells(self.p_list.words, self.p_list.words)
        self.progressbar()
    
        # (4): (3) with numbers: (aaabbb111)
        www_with_numbers = self.concatenate_two_lists_cells(words_with_words, self.p_list.numbers)
        self.progressbar()
    
        # (5): (1) before special characters: (aaa111@)
        one_before_spec = self.concatenate_two_lists_cells(words_before_numbers, self.p_list.spec_characters)
        self.progressbar()
    
        # (6): (4) with special characters: (aaabbb111@)
        self.concatenate_two_lists_cells(www_with_numbers, self.p_list.spec_characters)
        self.progressbar()
    
        # (7): (5) with numbers: (aaa111@111)
        self.concatenate_two_lists_cells(one_before_spec, self.p_list.numbers)
        self.progressbar()
    
        # (8): (5) with words: (aaa111@aaa)
        self.concatenate_two_lists_cells(one_before_spec, self.p_list.words)
        self.progressbar()
    
        # (9): words with (2): (aaa111222)
        words_with_three = self.concatenate_two_lists_cells(self.p_list.words, numbers_with_numbers)
        self.progressbar()
    
        # (10): (9) with special characters: (aaa111222@)
        self.concatenate_two_lists_cells(words_with_three, self.p_list.spec_characters)
        self.progressbar()
    
        # (11): (5) with special characters: (aaabbb@)
        self.concatenate_two_lists_cells(words_with_words, self.p_list.spec_characters)
        self.progressbar()

        self.zipFile()
        self.progressbar()

    def zipFile(self):
        zipname = self.filename.split('.')[0]
        zipfile.ZipFile('%s.zip' % zipname, mode='w').write(self.filename)
        
    def get_special_camel_case(self, word):
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
    
    def init_list(self, list):
        rlist = []
        for index in range(len(list)):
            if self.wordMinLen <= len(list[index]) <= self.wordMaxLen:
                new_words = self.get_special_camel_case(list[index])
                rlist.extend(new_words)
        rlist.extend(list)
    
        self.write_words_to_dictionary(rlist)
        return rlist  
    
    def concatenate_two_lists_cells(self, list_before, list_after):
        """ gets two lists and concatenate each cell in the list_before to a cell in the list_after.
            the function returns a list of the concatenated words."""
    
        rlist = []
    
        if len(list_before) == 0 or len(list_after) == 0:
            return rlist
    
        for index_before_list in range(len(list_before)):
            for index_after_list in range(len(list_after)):
                new_word = str(list_before[index_before_list]) + str(list_after[index_after_list])

                if self.wordMinLen <= len(new_word) <= self.wordMaxLen:
                    new_words_camel_case = self.get_special_camel_case(new_word)
                    rlist.append(new_word)
                    rlist.extend(new_words_camel_case)
    
        self.write_words_to_dictionary(rlist)
        return rlist
     
    def write_words_to_dictionary(self, words):
        """ writes a list of words to the self.filename specified"""
        with open(self.filename, "a") as dict:
            for word in words:
                dict.write(word + "\n")

    # ============================== More Functions ================================


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
    regex = re.compile(r'^[A-Za-z0-9]+[\S]*')
    data = list(filter(regex.search, data))
    print("in clean result:", data)
    return data


def split_by_separator(data):
    """ gets a data divided by separators that are not words characters
    and returns a list of the words separated"""
    return re.compile(r'\W+').split(data)

