import json


def create_file(file_path):
    """This function creates an empty JSON file, if the file does not already exist.
    If the file does exist, it does nothing and continues without raising an error.
    """
    try:
        with open(file_path, 'x') as file:
            json.dump([], file)  # initialize file as empty list
    except FileExistsError:
        pass


def _file_exists(file_path):
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        return False


def load_file(file_path):
    """ Loads a JSON file """
    if not _file_exists(file_path):
        create_file(file_path)
    with open(file_path, "r") as handle:
        data = json.load(handle)
    return data


def save_file(filename, data):
    """Creates a new json file with the given file name and writes the provided content to it."""
    try:
        with open(filename, 'w') as handle:
            json.dump(data, handle)
            return filename

    except Exception as e:
        print(f'Error message: {str(e)}')
