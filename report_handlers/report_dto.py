"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This class is to be more organized on controlling which label has which
    value for the final report and to use all its attributes as label-value
    pairs for generating in the csv
"""


class ReportDto:
    """
    Report Dto class will only present attributes for populating and accessing
    data required in the final report. There is one attribute per each value
    we want to present in the final csv
    """
    def __init__(self):
        self.n_lines = ['# of Lines', 0]
        self.n_words = ['# of Words', 0]
        self.n_digits = ['# of Digits', 0]
        self.n_characters = ['# of Characters', 0]
        self.n_filler_words = ['# of Filler Words', 0]
        self.n_invalid_words = ['# Words not found in dict', 0]
        self.n_punct_chars = ['# Punctuation characters', 0]
        self.n_upper_chars = ['# Upper characters', 0]
        self.n_lower_chars = ['# Lower characters', 0]
        self.n_unique_words = ['# Unique words', 0]
        self.most_used_words = ['Most used words', []]
        self.least_used_words = ['Least used words', []]
        self.most_used_letters = ['Most used letters', []]
        self.least_used_letters = ['Least used letters', []]
        self.most_used_fillers = ['Most used fillers', []]
        self.invalid_words = ['Words not found in dict', []]
        self.most_used_nums = ['Most used numbers', []]
