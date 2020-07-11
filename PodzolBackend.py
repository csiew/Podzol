import os
import json
from XmlFeed import XmlFeed

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
    
    def write_json(self, path, data_dict):
        error_msg = "Error: Unable to write to path - " + path
        with open(path, "wb", encoding="utf-8") as output_file:
            try:
                json.dump(data_dict, output_file, ensure_ascii=False, indent=4)
                return 0
            except:
                print(error_msg)
                pass
            return 1

    def get_feeds_path(self):
        return INDEX_STORE_PATH + FEEDS_INDEX_PATH

    def get_episodes_path(self):
        return INDEX_STORE_PATH + EPISODE_INDEX_PATH

    def read_feeds_index(self):
        return self.read_json(self.get_feeds_path())

    def read_episodes_index(self):
        return self.read_json(self.get_episodes_path())
    
    def update_feed_index(self):
        if self.data_index is not None:
            self.write_json(self.get_feeds_path(), self.data_index.feeds.items)
            return 0
        return 1
    
    def update_episodes_index(self, data_dict):
        if self.data_index is not None:
            self.write_json(self.get_episodes_path(), self.data_index.episodes.items)
            return 0
        return 1
    
    def add_podcast(self, url):
        try:
            feed, episodes = XmlFeed(url=url).parse()
        except:
            return 1
        self.data_index.feeds.items.append(feed)
        self.data_index.episodes.items.append(episodes)
        self.update_feed_index()
        self.update_episodes_index()
        return 0

    def main(self):
        debug_print("Reading JSON indexes...")
        feeds_index_dict = self.read_feeds_index()
        if feeds_index_dict is None:
            feeds_index = []
        episodes_index_dict = self.read_episodes_index()
        if episodes_index_dict is None:
            episodes_index = []

        if feeds_index_dict is not None and episodes_index_dict is not None:
            debug_print("Converting indexes...")
            feeds_index = FeedsIndex(feeds_index_dict)
            episodes_index = EpisodesIndex(episodes_index_dict)
            self.data_index = DataIndex(feeds_index, episodes_index)
        else:
            print("Error: Unable to read indexes!")
            return 1

        return 0


if __name__ == "__main__":
    Podzol().main()
