"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the text_dict_extractor class, which is in charge of extracting all
    the useful data for the report we are going to output, such as the number
    of occurrences of numbers, lines, words, etc. And will handle both globally
    and per line, this way we can identify in which line something interesting
    is detected. Interpretations are handled externally
"""
import string
from typing import List, Tuple, Dict


class TextDictExtractor:
    """
    Text dict extractor will get a list of lines and will transform those lines
    into many fields of statistics from the file we want to report, it will
    manage as attributes some count attributes for easy access
    """
    # Constants
    NEW_LINE_CHAR = '\n'
    NUM_CHARS = {str(n) for n in range(10)}
    THOUSANDS_SEP = ','
    DECIMAL_SEP = '.'
    THOUSAND_INTERVAL_LEN = 3

    def __init__(self, punctuation_chars):
        """
        Initialize both private and public attributes
        """
        # Private attributes
        self.__punctuation_chars = punctuation_chars
        # Public attributes
        self.all_char_dict = dict()
        self.all_word_dict = dict()
        self.all_numbers_dict = dict()
        self.n_punct_count = 0
        self.n_digit_count = 0
        self.n_upper_count = 0
        self.n_lower_count = 0

    def __repr__(self):
        return f'TextDictExtractor(Current chars counted as punctuation: ' \
               f'{self.__punctuation_chars}.\nAll chars dict truncated to ' \
               f'first 5 elements {self.all_char_dict.items()[:5]}.\nAll ' \
               f'words dict truncated to first 5 elements ' \
               f'{self.all_word_dict.items()[:5]}.\nAll numbers dict ' \
               f'truncated to first 5 numbers ' \
               f'{self.all_numbers_dict.items()[:5]}. Counts for char ' \
               f'types: Lowers: {self.n_lower_count} Uppers: ' \
               f'{self.n_upper_count} Punctuations: {self.n_punct_count} ' \
               f'Digits: {self.n_digit_count})'

    def is_valid_number(self, num_str: str) -> bool:
        """
        This method will accept any string number, either be decimal or with
        comma notation or both. It will accept the number if it is correctly
        formatted and return True, else it will return False.
        """
        # Split number to normal and decimal part, if it is integer, it will
        # still have 1 index
        split_num = num_str.split(self.DECIMAL_SEP)
        # Send integer part to comma notation detection and will return the
        # same number if correctly formatted
        split_num[0] = self.__comma_notation_to_num(split_num[0])
        # Number with comma notation is poorly formatted
        if split_num[0] is None:
            return False
        # It is not a valid decimal or integer number
        if len(split_num) > 2:
            return False
        # After getting rid of all middle characters, check if it is a number
        for n in split_num:
            if not n.isdigit():
                return False
        return True

    def __comma_notation_to_num(self, num_str: str):
        """
        This private method will check if the number is formatted in comma
        notation (E.g: 1,000,000) and will validate if it is correctly made
        """
        # If string does not have a comma, skip validations
        if self.THOUSANDS_SEP not in num_str:
            return num_str
        # Make a list of each interval inside comma separators
        num_list = num_str.split(self.THOUSANDS_SEP)
        # The first number should have no more than 3 digits
        if len(num_list[0]) > 3:
            return None
        # Intervals after first incidence should be only of length of 3
        for sub_num in num_list[1:]:
            if len(sub_num) != self.THOUSAND_INTERVAL_LEN:
                return None
        # Everything is correct, return number without commas for next step
        return ''.join(num_list)

    def __classify_char_in_counts(self, c: str):
        """
        Sends char count to one of counter attributes for using that data later
        """
        # It is a punctuation char
        if c in string.punctuation:
            self.n_punct_count += 1
        # It is a digit char
        elif c.isdigit():
            self.n_digit_count += 1
        # It is an upper char
        elif c.isupper():
            self.n_upper_count += 1
        # It is a lower char
        elif c.islower():
            self.n_lower_count += 1

    def __increase_record_count(self, target_dict: dict, record: str):
        """
        This private helper method increases the count for a target dict with
        a defined record label by 1. This method saves some lines as it is
        needed in many parts of the class
        """
        target_dict[record] = target_dict.get(record, 0) + 1

    def __get_sentence_data(self, pure_sentence: str) -> dict:
        """
        This private method saves the frequency of each letter, char and number
        on separate dicts respectively, it does all this in one iteration in
        order to have some efficiency in the program instead of iterating more
        than once through the contents of each sentence
        """
        word_dict = dict()
        for word in pure_sentence.split():
            # Iterate through each character in each word
            for c in word:
                # Add count to global file dict for final report
                self.__increase_record_count(self.all_char_dict, c)
                self.__classify_char_in_counts(c)
            # Format word removing any punctuation char at the beginning and
            # ending for having valid words
            new_word = word.strip(self.__punctuation_chars).lower()
            # Check if word is not an empty string
            if not new_word:
                continue
            # Check if 'word' has numbers, it will not be counted for dict
            # checking
            if set(new_word).intersection(self.NUM_CHARS):
                # If 'word' may be a number, save it in numbers dict
                if self.is_valid_number(new_word):
                    self.__increase_record_count(self.all_numbers_dict,
                                                 new_word)
                    continue
            # Add pure word to local and global word count
            self.__increase_record_count(word_dict, new_word)
            self.__increase_record_count(self.all_word_dict, new_word)
        # Return both word and char count dictionaries
        return word_dict

    def get_data_per_sentence(self, sentences: List[str]) -> Tuple[Dict]:
        """
        This is the public method which will be called to extract all necessary
        data for reporting from a sentence list
        """
        # Cycle through each sentence for extracting useful data
        data_per_sentence = []
        for sentence in sentences:
            # Prepare each sentence removing new line characters at the end
            pure_sentence = sentence.rstrip('\n')
            # Call private function for extracting word and letter dicts
            word_count = self.__get_sentence_data(pure_sentence)
            data_per_sentence.append(word_count)
        # Return tuple of word dictionaries per sentence
        return tuple(data_per_sentence)


# Unit test
if __name__ == '__main__':
    # Test constants
    TEST_VALID_NUMBER = '123,030.12'
    TEST_INVALID_NUMBER = '1984,234.4'
    TEST_LIST = [f'this is a sample sentence with, bad grammar. '
                 f'And punctuation\n', 'test sentence (No context needed)\n',
                 f'Another test sentence with number: {TEST_VALID_NUMBER} and'
                 f' an invalid one: {TEST_INVALID_NUMBER}\n']
    # Instantiate class for test
    text_dict_extractor = TextDictExtractor(string.punctuation)
    # Process sample data
    data = text_dict_extractor.get_data_per_sentence(TEST_LIST)
    # Verify statistics were generated
    assert len(data) == len(TEST_LIST)
    assert isinstance(data, tuple)
    assert all(isinstance(line, dict) for line in data)
    assert TEST_VALID_NUMBER in text_dict_extractor.all_numbers_dict
    assert TEST_INVALID_NUMBER not in text_dict_extractor.all_numbers_dict
    assert text_dict_extractor.all_word_dict
    assert 'a' in text_dict_extractor.all_word_dict
    assert 'a' in text_dict_extractor.all_char_dict
    assert text_dict_extractor.n_digit_count > 0
    assert text_dict_extractor.n_punct_count > 0
    assert text_dict_extractor.n_upper_count > 0
    assert text_dict_extractor.n_lower_count > 0
    print('Unit test passed successfully!')
