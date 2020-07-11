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

    def podzol_shell(self):
        primary_commands = ["exit", "help", "list"]
        operations = {
            "list": ["feeds", "episodes"]
        }

        while 1:
            command_string = input("podzol: ")
            command = command_string.split()
            if len(command) > 0 and command[0] in primary_commands:
                debug_print("Parsed command: " + str(command))
                if command[0] == "exit":
                    exit(0)
                elif command[0] == "help":
                    for item in primary_commands:
                        print("- " + item)
                        if item in operations.keys():
                            for subitem in operations[item]:
                                print("  - " + subitem)
                elif command[0] == "list":
                    if len(command) >= 2 and command[1] in operations["list"] and self.data_index is not None:
                        if command[1] == "feeds":
                            print(self.data_index.feeds.list())
                        elif command[1] == "episodes":
                            print(self.data_index.episodes.list())

    def main(self):
        debug_print("Reading JSON indexes...")
        feeds_index_dict = self.read_feeds_index()
        episodes_index_dict = self.read_episodes_index()

        if feeds_index_dict is not None and episodes_index_dict is not None:
            debug_print("Converting indexes...")
            feeds_index = FeedsIndex(feeds_index_dict)
            episodes_index = EpisodesIndex(episodes_index_dict)
            self.data_index = DataIndex(feeds_index, episodes_index)
            try:
                self.podzol_shell()
            except KeyboardInterrupt:
                debug_print("\nExiting Podzol...")
                exit(0)
        else:
            print("Error: Unable to read indexes!")
            return 1


if __name__ == "__main__":
    Podzol().main()
