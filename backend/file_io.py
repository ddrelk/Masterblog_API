import json


def load_file(file_path):
    """ Loads a JSON file """
    try:
        with open(file_path, "r") as handle:
            data = json.load(handle)
        return data

    except Exception as e:
        print(f'Error message: {str(e)}')


def save_file(filename, data):
    """Creates a new json file with the given file name and writes the provided content to it."""
    try:
        with open(filename, 'w') as handle:
            json.dump(data, handle)
            return filename

    except Exception as e:
        print(f'Error message: {str(e)}')
