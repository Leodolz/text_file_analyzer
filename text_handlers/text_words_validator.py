"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the TextWordsValidator class, which will validate if the words
    are valid or if these are filler words
"""
import os
from typing import Tuple, Dict, List

from exceptions import DependencyInitializationError
from input_handlers import FilesHandler
import json


class TextWordsValidator:
    """
    TextWordsValidator will validate words and classify filler words using
    two json files as source of criteria, its service will return invalid and
    filler words with the line of incidence per word
    """
    # Class constants
    HYPHENS_SYMBOL = '-'
    SINGLE_QUOTES_TRANSLATION = str.maketrans('', '', "'")

    def __init__(self, file_helper: FilesHandler, word_files_folder: str,
                 valid_words_file: str, filler_words_file: str):
        """
        Initialize class by opening both valid words and filler words json
        files and load them as dictionaries for searching quickly words not
        belonging to dicts
        """
        # Open and load files to dicts
        all_words_handler = file_helper.get_file_handler(valid_words_file,
                                                         word_files_folder)
        filler_words_handler = file_helper.get_file_handler(filler_words_file,
                                                            word_files_folder)
        # If there was any kind of error
        if file_helper.success is False:
            raise DependencyInitializationError(f'Error reading valid words '
                                                f'dicts: '
                                                f'{file_helper.message}')
        # Load files as dicts and close handlers
        self.__filler_words: dict = json.load(filler_words_handler)
        filler_words_handler.close()
        self.__valid_words: dict = json.load(all_words_handler)
        all_words_handler.close()

    def analyze_words_in_dict(self, words_list: Tuple[Dict]
                              ) -> Tuple[List, List]:
        """
        This method will classify each word of a list and will return two lists
        that will tell the user if each word is invalid or filler and the line
        it can be found
        """
        # Initialize lists
        not_found_words = []
        filler_words = []
        # Iterate through each word and classify if invalid or filler
        for i, line in enumerate(words_list):
            for word in line:
                # Call private method for classification
                self.__append_if_not_found(not_found_words, filler_words,
                                           word, i + 1)

        return not_found_words, filler_words

    def __append_if_not_found(self, invalid_list: list, filler_list: list,
                              word: str, line: int) -> None:
        """
        Private method which acts as a helper for the analyzer which will act
        as a recursive function in case that the word is composed with hyphens
        and will validate each word given by adding it to the respective list
        if it fulfills any of the invalid or filler criteria
        """
        # If there is no word, nothing to do
        if not word:
            return
        # If word has single quotes, return a new string removing those, also
        # transform word to lower for better comparison
        word = word.translate(self.SINGLE_QUOTES_TRANSLATION).lower()
        # If it has hyphens, separate words and call the method recursively
        if self.HYPHENS_SYMBOL in word:
            for sub_word in word.split(self.HYPHENS_SYMBOL):
                self.__append_if_not_found(invalid_list, filler_list,
                                           sub_word, line)
        # Verify if word is found in english dictionary
        elif self.__valid_words.get(word) is None:
            invalid_list.append((word, line))
        # Verify if word is found in filler dictionary
        elif self.__filler_words.get(word) is not None:
            filler_list.append((word, line))


# Unit test
if __name__ == '__main__':
    # Test constants
    INPUT_FOLDER = 'files_input'
    WORDS_FOLDER = 'valid_words'
    WORDS_FILE = 'english_words.json'
    FILLER_WORDS_FILE = 'filler_words.json'
    N_DEFAULT_FILES = 10
    JSON_FORMAT = '.json'
    PROJECT_DIR = os.path.dirname(os.getcwd())
    # Instantiate files handler dependency
    text_word_validator = TextWordsValidator(FilesHandler(N_DEFAULT_FILES,
                                                          JSON_FORMAT,
                                                          PROJECT_DIR),
                                             WORDS_FOLDER,
                                             WORDS_FILE,
                                             FILLER_WORDS_FILE)
    # Create sample data
    SAMPLE_DATA_PER_SENTENCE = (
        {'this': 5, "don't": 3, 'usually': 4, 'magnaneous': 1, 'inbalid': 3},
        {'sample': 2, 'ironically': 1, 'When': 5, 'abc123': 1},
        {'responsible': 2, 'together': 1, 'Rigorous': 3, 'Nolsa': 4, 'THAT': 3}
    )
    # Call analyzer and assign results to invalid and filler lists
    invalid_words, filler_words = text_word_validator.\
        analyze_words_in_dict(SAMPLE_DATA_PER_SENTENCE)
    # Assert data was generated as we introduced invalid and filler words in
    # sample
    assert len(invalid_words) > 0
    assert len(filler_words) > 0
    assert isinstance(invalid_words, list)
    assert isinstance(filler_words, list)
    print('Unit test passed successfully!')
