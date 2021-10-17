"""
    Elmer Leandro Hurtado Dolz
    Class: CS 521 - Fall 1
    Date: October 17th, 2021
    Final project
    This is the files handler class, which will be in charge of reading an
    individual file for returning text lines, it will also validate any issue
    related to expected file size and extension, it will check if the file
    exists too. The message and success attributes are public and can be
    accessed from caller to handle failures or success
"""
import os
from typing import TextIO

# Constants
DEFAULT_MAX_FILE_SIZE_MB = 50
DEFAULT_FILE_EXTENSION = '.txt'
STATUS_DICT = {True: 'OK', False: 'FAILED'}


class FilesHandler:
    """
    Files handler class handles validation and content of a specified file, its
    initialization can be set with some config values such as max file size
    and the file extension we want to focus on
    """

    def __init__(self, max_file_size_mb=DEFAULT_MAX_FILE_SIZE_MB,
                 file_extension=DEFAULT_FILE_EXTENSION,
                 current_dir=os.getcwd()):
        """
        Initialize both private and public attributes
        """
        self.__file_extension = file_extension
        self.__max_file_length_mb = max_file_size_mb
        self.__current_dir = current_dir
        self.message = ''
        self.success = True

    def __repr__(self):
        """
        Implement repr function to describe what this class needs and the
        # current state of it
        """
        return f'FilesHandler(Expected file extension = ' \
               f'{self.__file_extension}, Maximum file length admitted = ' \
               f'{self.__max_file_length_mb} MB, Current message = ' \
               f'{self.message}, Current success state = {self.success})'

    def __str__(self):
        """
        Implement str function for printing useful value for other classes
        describing its current state
        """

        return f'File reading status: {STATUS_DICT[self.success]}. Details: ' \
               f'{self.message}'

    def __validate_file(self, file_name: str, file_dir: str) -> bool:
        """
        This function validates that the file has the admitted extension and
        that the file does not surpass the defined maximum length
        """
        # File name does not end with file extension defined in attributes
        if file_name[-len(self.__file_extension):] != self.__file_extension:
            self.message = f'File {file_name} does not end with expected ' \
                           f'extension: {self.__file_extension}'
            return False
        # File size is bigger than admitted max size
        if os.path.getsize(file_dir) > self.__max_file_length_mb * 1e6:
            self.message = f'File {file_name} is bigger than expected, ' \
                           f'max size is: {self.__max_file_length_mb} MB'
            return False
        return True

    def get_file_contents(self, file_name: str, folder: str) -> list or None:
        """
        For getting contents, first call the file handler object so
        everything is validated first, check that handler exists and by correct
        file handling, the function reads from object and returns contents
        """
        file_handler = self.get_file_handler(file_name, folder)
        if file_handler is None:
            return None
        file_contents = file_handler.readlines()
        file_handler.close()

        return file_contents

    def get_file_handler(self, file_name: str, folder: str) -> TextIO or None:
        """
        This functions will call internal methods to validate and then extract
        the file object for external handling, if anything happens such as an
        exception or bad validation, the class will set its attributes to the
        respective state for external error printing
        """
        file_dir = os.path.join(self.__current_dir, folder, file_name)
        try:
            # Call private method to validate file extension and size
            if self.__validate_file(file_name, file_dir) is False:
                # If validation fails, set success attribute to false
                self.success = False
                return None
            # Return file handling object, remember to close it after usage
            return open(file_dir, 'r')
        except FileNotFoundError as e:
            # Catch file not found error even from validation call and set
            # Message and Success attributes to its respective failure
            self.message = f'File: {file_name} does not exist in current ' \
                           f'({self.__current_dir}) directory'
            self.success = False
            return None


# Unit test
if __name__ == '__main__':
    # Test constants
    TEST_FILE_STR = 'test.txt'
    TEST_FOLDER = 'test'
    # Instantiate files handler for testing
    files_handler = FilesHandler(current_dir=os.path.dirname(os.getcwd()))
    # Get contents from valid file inside test folder
    test_contents = files_handler.get_file_contents(TEST_FILE_STR, TEST_FOLDER)
    # Assert everything went correct with contents as output
    assert files_handler.success
    assert files_handler.message == ''
    assert isinstance(test_contents, list) and len(test_contents) > 0
    # Make invalid file test case where files should have and error message
    invalid_contents = files_handler.get_file_contents('invalid.txt',
                                                       TEST_FOLDER)
    # Assert success was false and there was an error message
    assert files_handler.success is False
    assert files_handler.message != ''
    # Assert no contents were delivered because of invalid input
    assert invalid_contents is None
    print('Unit test passed successfully!')
