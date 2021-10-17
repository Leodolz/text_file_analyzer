"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the files input directory handler class, which will be in charge of
    validating the correct directories are referenced and that the internal
    rules are applied to directories such as the max amount of files inside
    the input folder and will handle the names of the valid text files inside
    the directory
"""
import os

# Constants
DEFAULT_MAX_SIZE = 15
DEFAULT_INPUT_FOLDER_NAME = 'files_input/'


class InputDirectoryHandler:
    """
    This class will handle files inside a constant input folder and validate
    some inner rules configured in constructor
    """
    def __init__(self, max_file_units=DEFAULT_MAX_SIZE,
                 current_dir=os.getcwd()):
        """
        Initialize class with config for max file units in directory defined
        """
        self.__current_dir = current_dir
        self.__max_file_units = max_file_units

    def __repr__(self):
        """
        Format its repr implementation for more readability
        """
        return f'InputDirectoryHandler(Maximum number of files inside ' \
               f'folder = {self.__max_file_units} files)'

    def __validate_directory_input(self, list_dir: list) -> bool:
        """
        Validate that folder does not have more files than configured
        """
        if len(list_dir) <= self.__max_file_units:
            return True
        return False

    def get_directory_filenames(self,
                                input_directory=DEFAULT_INPUT_FOLDER_NAME
                                ) -> list:
        """
        Method in charge of returning all text files inside folder
        """
        # Get current working directory's input folder
        abs_file_dir = os.path.join(self.__current_dir, input_directory)
        # If directory does not exist, create one
        if not os.path.isdir(abs_file_dir):
            os.mkdir(abs_file_dir)
            return []
        # List all files inside folder
        text_files = [file_name for file_name in os.listdir(abs_file_dir)]
        # Validate if file list fulfills criteria of max units
        if self.__validate_directory_input(text_files):
            return text_files
        # If not, return empty list for finishing execution
        return []


# Unit test
if __name__ == '__main__':
    # Test constants
    TEST_FOLDER = 'test/'
    PROJECT_DIR = os.path.dirname(os.getcwd())
    # Instantiate class for unit test
    input_directory_handler = InputDirectoryHandler(current_dir=PROJECT_DIR)
    # Get files list
    files = input_directory_handler.get_directory_filenames(TEST_FOLDER)
    assert len(files) > 0
    assert all([isinstance(file, str) for file in files])
    print('Unit test passed successfully!')
