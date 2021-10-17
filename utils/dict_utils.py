"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the dict class file which will act as a helper to process dict
    items and format or modify structure for usage
"""
from typing import List, Tuple
from operator import itemgetter

VALUE_IDX = 1


class DictUtils:
    """
    Helper class that will help other parts of the program for formatting or
    rearranging dictionary structures or its item structures (List[Tuple])
    """
    def format_dict_items(self, target_dict_items: List[Tuple]):
        """
        Function to return a formatted list of items ready for printing
        or presenting at final report
        """
        formatted_list = []
        for k, v in target_dict_items:
            # Format time or times depending on plurals
            time_tense = 'time'
            if v > 1:
                time_tense += 's'
            # Append formatted item to final list
            formatted_list.append(f'"{k.title()}": {v} {time_tense}')
        return formatted_list

    def get_sorted_by_value(self, target_dict_items: List[Tuple]):
        """
        Function to return a sorted list of items from a dictionary's items
        having its sorting by value instead of by key
        """
        return sorted(target_dict_items, key=itemgetter(VALUE_IDX))


# Unit test
if __name__ == '__main__':
    SAMPLE_DICT = {'ABC': 3, 'The': 1, 'hello': 2}
    dict_utils = DictUtils()
    sorted_items = dict_utils.get_sorted_by_value(SAMPLE_DICT.items())
    formatted_list = dict_utils.format_dict_items(SAMPLE_DICT.items())
    assert sorted_items[0][1] == 1
    assert 'times' in formatted_list[0]
    assert 'times' not in formatted_list[1]
    print('Unit test passed successfully!')
