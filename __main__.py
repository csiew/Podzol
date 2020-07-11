import os
import json

from DataIndex import DataIndex
from FeedsIndex import FeedsIndex
from EpisodesIndex import EpisodesIndex

INDEX_STORE_PATH = "data/"
FEEDS_INDEX_PATH = "feeds.json"
EPISODE_INDEX_PATH = "episodes.json"

data_index = None


def get_feeds_path():
    return INDEX_STORE_PATH + FEEDS_INDEX_PATH


def get_episodes_path():
    return INDEX_STORE_PATH + EPISODE_INDEX_PATH


def read_json(path):
    error_msg = "Error: Unable to read path - " + path
    if os.path.exists(path):
        with open(path, "r") as json_dict:
            try:
                json_dict = json.load(json_dict)
                return json_dict
            except:
                print(error_msg)
                pass
            return None
    else:
        print(error_msg)
        return None


def read_feeds_index():
    return read_json(get_feeds_path())


def read_episodes_index():
    return read_json(get_episodes_path())


def podzol_shell():
    while 1:
        command = input("podzol: ")
        print(command)


def main():
    global data_index

    print("Reading JSON indexes...")
    feeds_index_dict = read_feeds_index()
    episodes_index_dict = read_episodes_index()

    if feeds_index_dict is not None and episodes_index_dict is not None:
        print("Converting indexes...")
        feeds_index = FeedsIndex(feeds_index_dict)
        episodes_index = EpisodesIndex(episodes_index_dict)
        data_index = DataIndex(feeds_index, episodes_index)
        try:
            podzol_shell()
        except KeyboardInterrupt:
            print("\nExiting Podzol...")
            exit(0)
    else:
        print("Error: Unable to read indexes!")
        return 1


if __name__ == "__main__":
    main()
