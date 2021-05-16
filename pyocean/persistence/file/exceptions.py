#! /etc/anaconda/python3


class FilePathCannotBeEmpty(Exception):

    def __str__(self):
        return "File path shouldn't be empty."


class ClassNotInstanceOfBaseFileFormatter(TypeError):

    def __str__(self):
        return "Class isn't the instance of BaseFileFormatter type."


class NotSupportHandlingFileType(Exception):

    def __str__(self):
        return "It doesn't support to handle the file type currently. Please use JSON, CSV or Excel type file."

