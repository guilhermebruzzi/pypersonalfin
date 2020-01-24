import os
import pathlib

root_folder = pathlib.Path(__file__).parent.parent.parent
src_folder = root_folder / 'pypersonalfin'
data_folder = root_folder / 'data'
output_folder = root_folder / 'output'


def _get_abs_path(file_name, folder):
    if file_name:
        return (folder / file_name).absolute()
    return folder.absolute()


def get_data_folder_abs_path(file_name):
    return _get_abs_path(file_name=file_name, folder=data_folder)


def get_output_folder_abs_path(file_name):
    return _get_abs_path(file_name=file_name, folder=output_folder)


def get_src_folder_abs_path(file_name):
    return _get_abs_path(file_name=file_name, folder=src_folder)


def get_files_of_data_folder(glob):
    return data_folder.glob(glob)


def get_file_content(file_path):
    with open(file_path) as f:
        return f.read()


def save_file_content(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def save_file_on_output_folder(file_name, content):
    file_path = get_output_folder_abs_path(file_name)
    save_file_content(file_path, content)
