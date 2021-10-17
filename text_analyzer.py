"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the main program which will execute file readers, collections
    handlers, text formatters, etc. to give a final report for statistics
    on one or more txt files given inside the directory ./files_input/
"""
import string

from exceptions import DependencyInitializationError
from input_handlers import FilesHandler, \
    InputDirectoryHandler
from report_handlers import CsvDataPreProcessor, \
    CsvReporter
from text_handlers import TextDictExtractor, \
    TextWordsValidator
from utils import DictUtils

INPUT_FOLDER = 'files_input'
WORDS_FOLDER = 'valid_words'
WORDS_FILE = 'english_words.json'
FILLER_WORDS_FILE = 'filler_words.json'
N_DEFAULT_FILES = 10
JSON_FORMAT = '.json'
EXIT_KEY = '0'
LINE_WIDTH = 80
INPUT_MESSAGE = f'{"-"*LINE_WIDTH}\n' \
                f'For processing files, please place some inside ' \
                f'{INPUT_FOLDER} folder.\nThen press enter key to start. If ' \
                f'you wish to exit program, enter "{EXIT_KEY}": '


def initialize_services():
    """
    Initialize dependencies which are going to be used for project
    """
    in_handler = InputDirectoryHandler()
    file_handler = FilesHandler()
    data_extractor = TextDictExtractor(string.punctuation)
    dict_util = DictUtils()

    text_word_validator = TextWordsValidator(FilesHandler(N_DEFAULT_FILES,
                                                          JSON_FORMAT),
                                             WORDS_FOLDER,
                                             WORDS_FILE,
                                             FILLER_WORDS_FILE)
    csv_reporter = CsvReporter()
    return in_handler, file_handler, data_extractor, dict_util, \
           text_word_validator, csv_reporter


if __name__ == '__main__':
    try:
        # Create instances of all dependencies in the project
        input_handler, files_handler, text_data_extractor, dict_utils, \
        text_words_validator, csv_reporter = initialize_services()
        # Catch custom dependency error and print user-friendly error message
    except DependencyInitializationError as dependency_error:
        print(f'Error initializing dependencies for program: '
              f'{str(dependency_error)}. Please consider to re-download '
              f'project as it needs its json dependencies.')
        # If no error happened, start with data handling until report is done
    else:
        print('Welcome to text file analyzer!')
        print(f'Initialized input directory handler with current config:\n'
              f'{repr(input_handler)}')
        print(f'Initialized input file handler with current config:\n'
              f'{repr(input_handler)}')
        while input(INPUT_MESSAGE).strip() != EXIT_KEY:
            # Start getting all files from input directory
            files = input_handler.get_directory_filenames()
            for text_file in files:
                # For each file, get its contents
                file_rows = files_handler.get_file_contents(text_file,
                                                            INPUT_FOLDER)
                # If content fetching failed, print error message and skip file
                if files_handler.success is False:
                    print(f'Error reading input file "{text_file}": \n'
                          f'{str(files_handler)}. Skipping file...')
                    continue
                # Start getting statistics from contents
                data_per_sentence = text_data_extractor. \
                    get_data_per_sentence(file_rows)
                if not data_per_sentence:
                    print(f'File {text_file} is empty, skipping it...')
                    continue
                # Validate found words with json file of english words
                invalid_words, filler_words = text_words_validator. \
                    analyze_words_in_dict(data_per_sentence)
                # Prepare data for report with csv processor instance, we are
                # creating instance with data from our extractor
                csv_preprocessor = CsvDataPreProcessor(text_data_extractor,
                                                       dict_utils)
                csv_preprocessor.process_data_for_report(len(data_per_sentence),
                                                         invalid_words,
                                                         filler_words)
                # With out csv preprocessor's dto attribute, we generate the
                # csv report passing the text name without extension
                csv_reporter.generate_report(csv_preprocessor.report_dto,
                                             text_file.split('.')[0])
            if len(files) < 1:
                print(f'No files were found inside input directory, please add '
                      f'some files for processing and run again')
            else:
                print(f'Finished processing {len(files)} files. Please check '
                      f'output inside output_reports/ folder')
