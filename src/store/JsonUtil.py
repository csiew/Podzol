import os
import json


def read_json(path):
    error_msg = "Unable to read path: " + path
    if os.path.exists(path):
        with open(path, "r") as json_dict:
            try:
                json_dict = json.load(json_dict)
                return json_dict
            except (RecursionError, TypeError, ValueError):
                print(error_msg)
                pass
            return None
    else:
        print(error_msg)
        return None


def write_json(path, data_dict):
    error_msg = "Unable to write to path: " + path
    with open(path, "w") as output_file:
        try:
            json.dump(data_dict, output_file)
            return 0
        except (RecursionError, TypeError, ValueError):
            print(error_msg)
            pass
        return 1


def make_dir(path):
    error_msg = "Unable to create dir at path: " + path
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Created directory at: " + path)
        else:
            print("Directory already exists at: " + path)
        return 0
    except OSError:
        print(error_msg)
        pass
    return 1
