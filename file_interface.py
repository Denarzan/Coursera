import os.path
from pathlib import Path
import tempfile
import uuid

"""interface for working with files"""


class File:
    def __init__(self, given_file):
        if not os.path.exists(given_file):  # creating new file if it's not exists
            with open(given_file, "w") as f:
                self.given_file = Path(given_file)
        else:
            self.given_file = Path(given_file)  # name of the file
        self.path_to_file = os.path.abspath(given_file)  # path to file

    def __str__(self):
        return self.path_to_file  # returns the full path to the file as a string representation

    def __add__(self, other_file):  # addition of objects of type File with creating new file
        with open(self.given_file, "r") as f:
            code = f.read()
        with open(other_file.given_file, "r") as f:
            another_code = f.read()
        temp_code = code + another_code
        temp = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        with open(temp, "w") as file:
            file.write(temp_code)  # new file has contents of both files
        new_object = File(temp)
        return new_object

    def __next__(self):  # maintain an iteration protocol, with the iteration going through the lines of the file
        with open(self.given_file, "r") as f:
            f.seek(self.current)
            line = f.readline()
            if not line:
                self.current = 0
                raise StopIteration
            self.current = f.tell()
            return line

    def __iter__(self):
        self.current = 0
        return self

    def read(self):  # returns the file content
        with open(self.given_file, "r") as f:
            return f.read()

    def write(self, text):  # takes as an argument a string with the new contents of the file
        with open(self.given_file, "w") as f:
            return f.write(text)


