"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the csv reporter class, which will be in charge of parsing ordered
    data into a csv file for each file on the input. It has a constant order
    of which the labels will be presented
"""
import os
from typing import Tuple, List

from report_handlers.report_dto import ReportDto
import csv

# Constant labels ordering
REPORT_LABELS = [
            'n_lines', 'most_used_words', 'n_words',
            'least_used_words', 'n_digits', 'most_used_letters',
            'n_characters', 'least_used_letters',
            'n_filler_words', 'most_used_fillers',
            'n_invalid_words', 'invalid_words', 'n_punct_chars',
            'most_used_nums', 'n_upper_chars', None,
            'n_lower_chars', None, 'n_unique_words', None
        ]


class CsvReporter:
    """
    Csv Reporter is in charge of generating a csv per file, it will present
    results based in the report dto and will generate headers, labels and
    values for presenting data in a human-readable way
    """
    def __generate_report_row(self, csv_writer,
                              items_left: Tuple[List],
                              items_right: Tuple[List]):
        """
        This method will accept a left side and right side element, which will
        both be inserted as a row with a whitespace in the middle for better
        reading
        """
        csv_writer.writerow([items_left[0], items_left[1], '',
                             items_right[0], items_right[1]])

    def __generate_report_rows(self, csv_writer, all_items):
        """
        Method that iteratively sends items as left and right side to previous
        method above, this will divide all items given into an ordered paired
        collection of items until the list iteration is finished
        """
        for i in range(0, len(all_items), 2):
            # Prepare two blank spaces for right items when no right side is
            # positioned on row. We use two blank because it represents a blank
            # label and a blank value
            items_right = [''] * 2
            # Make sure we do not go out of boundaries of list
            if i < len(all_items) - 1:
                # If next item is not none or empty
                if all_items[i + 1]:
                    # Assign right as next item
                    items_right = all_items[i + 1]
            # Call generate report row now that we have left and right
            self.__generate_report_row(csv_writer, all_items[i], items_right)

    def __get_report_structured_items(self, report_dto: ReportDto,
                                      item_labels: list):
        """
        Method in charge of fetching determined attributes from report dto
        and return them as a list of each of these attributes
        """
        structured_items = []
        for item_label in item_labels:
            # If we want a None value in the list
            if item_label is None:
                structured_items.append(None)
            # Get attribute from dto programmatically
            else:
                structured_items.append(
                    report_dto.__getattribute__(item_label)
                )
        # Returned attributes as ordered collection
        return structured_items

    def __populate_report_headers(self, csv_writer):
        """
        This method is in charge of writing the header part of the report,
        which will be the same for each report
        """
        csv_writer.writerow(['Count Data', '', '', 'Frequency Data', '', ''])
        csv_writer.writerow([])
        csv_writer.writerow(['Title', 'Value', '', 'Title', 'Value'])

    def generate_report(self, report_dto: ReportDto, text_name: str):
        """
        Method in charge of generating a csv report from an input text name
        and an already populated dto to use as source of info for the report
        """
        # If output directory does not exist, create one
        if not os.path.isdir('output_reports'):
            os.mkdir('output_reports')
        # Create the report file object in write mode
        report_file = open(f'output_reports/{text_name}.csv', 'w')
        # Handle file object to csv writer as we want a csv output
        csv_writer = csv.writer(report_file)
        # Write the constant headers for the report
        self.__populate_report_headers(csv_writer)
        # Get the items ordered and ready to write on report
        structured_items = self.__get_report_structured_items(report_dto,
                                                              REPORT_LABELS)
        # Write ordered info
        self.__generate_report_rows(csv_writer, structured_items)
        # Close file
        report_file.close()
