import os
import json

from DataIndex import DataIndex
from FeedsIndex import FeedsIndex
from EpisodesIndex import EpisodesIndex

DEBUG = True

INDEX_STORE_PATH = "data/"
FEEDS_INDEX_PATH = "feeds.json"
EPISODE_INDEX_PATH = "episodes.json"


def debug_print(msg):
    if DEBUG is True:
        print(msg)


class Podzol(object):
    def __init__(self):
        self.data_index = None

    def get_feeds_path(self):
        return INDEX_STORE_PATH + FEEDS_INDEX_PATH

    def get_episodes_path(self):
        return INDEX_STORE_PATH + EPISODE_INDEX_PATH

    def read_json(self, path):
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

    def read_feeds_index(self):
        return self.read_json(self.get_feeds_path())

    def read_episodes_index(self):
        return self.read_json(self.get_episodes_path())

    def main(self):
        debug_print("Reading JSON indexes...")
        feeds_index_dict = self.read_feeds_index()
        episodes_index_dict = self.read_episodes_index()

        if feeds_index_dict is not None and episodes_index_dict is not None:
            debug_print("Converting indexes...")
            feeds_index = FeedsIndex(feeds_index_dict)
            episodes_index = EpisodesIndex(episodes_index_dict)
            self.data_index = DataIndex(feeds_index, episodes_index)
        else:
            print("Error: Unable to read indexes!")
            return 1


if __name__ == "__main__":
    Podzol().main()
