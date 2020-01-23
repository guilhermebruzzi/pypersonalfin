import os
import pathlib

root_folder = pathlib.Path(__file__).parent.parent.parent
data_folder = root_folder / 'data'


def get_files_of_data_folder(glob):
    return data_folder.glob(glob)


def get_file_content(file_path):
    with open(file_path) as f:
        return f.read()
