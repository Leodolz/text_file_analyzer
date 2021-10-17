"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the script in charge of preprocessing info and making it ready
    for printing all in the report.
"""
import string
from typing import Tuple, List

from report_handlers.report_dto import ReportDto
from text_handlers import TextDictExtractor
from utils.dict_utils import DictUtils


class CsvDataPreProcessor:
    """
    Class managing report dto as new instance in the constructor for having
    different data per file and not having unwanted behavior when managing
    different files at once. It prepares data for reporting in csv
    """

    def __init__(self, text_data_extractor: TextDictExtractor,
                 dict_utils: DictUtils):
        self.report_dto = ReportDto()
        self.__dict_utils = dict_utils
        self.__text_data_extractor = text_data_extractor

    def __populate_count_data(self, n_lines: int,
                              invalid_words: List[Tuple],
                              filler_words: List[Tuple]):
        """
        This function populates the data relevant to counts on the report
        """
        # Populate report labels using sum of values for dicts and calculating
        # lengths of lists
        self.report_dto.n_lines[1] = n_lines
        self.report_dto.n_words[1] = sum(self.__text_data_extractor.
                                         all_word_dict.values())
        self.report_dto.n_characters[1] = sum(self.__text_data_extractor.
                                              all_char_dict.values())
        self.report_dto.n_invalid_words[1] = len(invalid_words)
        self.report_dto.n_filler_words[1] = len(filler_words)
        self.report_dto.n_unique_words[1] = len(self.__text_data_extractor.
                                                all_word_dict.keys())
        # Populate counts using public attributes of counters from text data
        # extractor
        self.report_dto.n_punct_chars[1] = self.__text_data_extractor.\
            n_punct_count
        self.report_dto.n_digits[1] = self.__text_data_extractor.n_digit_count
        self.report_dto.n_lower_chars[1] = self.__text_data_extractor. \
            n_lower_count
        self.report_dto.n_upper_chars[1] = self.__text_data_extractor. \
            n_upper_count

    def __get_label_value_pairs(self, ordered_words, ordered_letters,
                                ordered_nums, ordered_fillers,
                                ordered_invalid):
        """
        Return a list of pairs of items which are tuples with a nomenclature
        of first element to be a label and second element to be the values
        intended to be displayed in report
        """
        return [
            # For least used we slice the top 5 of first elements
            ('least_used_words', ordered_words[:5]),
            ('least_used_letters', ordered_letters[:5]),
            # For most used we slice the last 5 (As it is ordered from lowest
            # to highest), reversing its order to have from highest to lowest
            ('most_used_words', ordered_words[-1:-6:-1]),
            ('most_used_letters', ordered_letters[-1:-6:-1]),
            ('most_used_nums', ordered_nums[-1:-6:-1]),
            ('most_used_fillers', ordered_fillers[-1:-6:-1]),
            # Make a small formatting for invalid words and truncate to target
            # number of incidences
            ('invalid_words', [
                f'"{k}": At line {v}' for k, v in ordered_invalid]),
        ]

    def __populate_frequency_data(self, invalid_words: List[Tuple],
                                  filler_words: List[Tuple]):
        """
        This function populates the data relevant to frequencies related to
        words and numbers on the report, having ordering processes
        """
        # Get ordered items by value for words, letters, fillers, invalid words
        # and numbers
        ordered_words = self.__dict_utils.get_sorted_by_value(
            self.__text_data_extractor.all_word_dict.items())
        ordered_letters = self.__dict_utils.get_sorted_by_value(
            [(k, v) for k, v in self.__text_data_extractor.all_char_dict.
                items() if k not in string.punctuation])
        ordered_fillers = self.__dict_utils.get_sorted_by_value(filler_words)
        ordered_invalid = self.__dict_utils.get_sorted_by_value(invalid_words)
        ordered_nums = self.__dict_utils.get_sorted_by_value(
            self.__text_data_extractor.all_numbers_dict.items()
        )

        # Get list of pairs for next step
        freq_used_collection = self.__get_label_value_pairs(ordered_words,
                                                            ordered_letters,
                                                            ordered_nums,
                                                            ordered_fillers,
                                                            ordered_invalid)
        # Save ordered data as required in dto items, taking into account the
        # ordered items are from lowest to highest values
        self.__populate_freq_used_words(freq_used_collection)

    def __populate_freq_used_words(self, ordered_collections: List[Tuple]):
        """
        Method to populate dto with words by most or least used frequency
        saving formatted info in attributes, always pointing to value index
        """
        for ordered_collection in ordered_collections:
            # Use getattribute to programmatically access an attribute of
            # object
            freq_attr = self.report_dto.__getattribute__(ordered_collection[0])
            # If collection has a not none or empty value
            if ordered_collection[1]:
                freq_value_list = ordered_collection[1]
                # Check if the item is a tuple for accessing its label value
                if all(isinstance(e, tuple) for e in ordered_collection[1]):
                    # Format its dictionary items inside ordered collection
                    freq_value_list = self.__dict_utils.format_dict_items(
                        ordered_collection[1])
                # Save item list as a single string formatted for report
                freq_attr[1] = ",".join(freq_value_list)

    def process_data_for_report(self, n_lines: int,
                                invalid_words: List[Tuple],
                                filler_words: List[Tuple]):
        """
        Facade method which which breaks the task related to populating
        formatted data for report into smaller tasks. It has the "side effect"
        of having its public dto attribute populated and ready for csv
        """

        self.__populate_count_data(n_lines, invalid_words,
                                   filler_words)
        self.__populate_frequency_data(invalid_words, filler_words)


if __name__ == '__main__':
    # Instantiate class' dependencies
    dict_utils = DictUtils()
    text_data_extractor = TextDictExtractor(string.punctuation)
    # Create sample data for pre process
    text_data_extractor.all_char_dict = {'a': 1, 'c': 3, 'b': 2, '.': 5,
                                         '1': 1}
    text_data_extractor.all_word_dict = {'Hi': 2, 'sample': 1, 'this': 3}
    text_data_extractor.all_numbers_dict = {'123': 2, '10.34': 1}
    text_data_extractor.n_digit_count = 2
    csv_data_preprocessor = CsvDataPreProcessor(text_data_extractor,
                                                dict_utils)
    csv_data_preprocessor.process_data_for_report(2, [('cxs', 2)],
                                                  [('that', 1)])

    # Assert data is ready for report
    assert csv_data_preprocessor.report_dto.n_digits[1] == 2
    assert csv_data_preprocessor.report_dto.n_lines[1] == 2
    assert 'cxs' in csv_data_preprocessor.report_dto.invalid_words[1]
    assert 'That' in csv_data_preprocessor.report_dto.most_used_fillers[1]
    assert '3' in csv_data_preprocessor.report_dto.most_used_words[1]
    print('Unit test passed successfully!')
