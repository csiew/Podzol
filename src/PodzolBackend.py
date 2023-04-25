import os
from XmlFeed import XmlFeed

from Feed import Feed
from Episode import Episode
from DataIndex import DataIndex
from FeedsIndex import FeedsIndex
from EpisodesIndex import EpisodesIndex
from store.JsonUtil import read_json, write_json, make_dir

DEBUG = False

INDEX_STORE_PATH = "data/"
FEEDS_INDEX_PATH = "feeds.json"
EPISODE_INDEX_PATH = "episodes.json"


def debug_print(msg):
    if DEBUG is True:
        print(msg)


class Podzol(object):
    def __init__(self):
        self.data_index = None

    @staticmethod
    def get_data_dir_path():
        return INDEX_STORE_PATH

    @staticmethod
    def get_feeds_path():
        return INDEX_STORE_PATH + FEEDS_INDEX_PATH

    @staticmethod
    def get_episodes_path():
        return INDEX_STORE_PATH + EPISODE_INDEX_PATH
    
    def purge(self):
        try:
            write_json(self.get_feeds_path(), [])
            write_json(self.get_episodes_path(), [])
        except:
            return 1
        return 0

    def create_data_dir_if_not_exists(self):
        make_dir(self.get_data_dir_path())

    def create_feeds_index(self):
        self.create_data_dir_if_not_exists()
        feeds_path = self.get_feeds_path()
        with open(feeds_path, "x") as output_file:
            try:
                output_file.write("[]")
                print("Created file at: " + feeds_path)
                return 0
            except IOError:
                print("Failed to create feeds index file")
                pass
        return 1

    def create_episodes_index(self):
        self.create_data_dir_if_not_exists()
        episodes_path = self.get_episodes_path()
        with open(episodes_path, "x") as output_file:
            try:
                output_file.write("[]")
                print("Created file at: " + episodes_path)
                return 0
            except IOError:
                print("Failed to create episodes index file")
                pass
        return 1

    def read_feeds_index(self):
        if not os.path.exists(self.get_feeds_path()):
            self.create_feeds_index()
        return read_json(self.get_feeds_path())

    def read_episodes_index(self):
        if not os.path.exists(self.get_episodes_path()):
            self.create_episodes_index()
        return read_json(self.get_episodes_path())
    
    def update_feed_index(self):
        if self.data_index is not None:
            write_json(self.get_feeds_path(), self.data_index.feeds.as_dict())
            return 0
        return 1
    
    def update_episodes_index(self):
        if self.data_index is not None:
            write_json(self.get_episodes_path(), self.data_index.episodes.as_dict())
            return 0
        return 1
    
    def update_indexes(self):
        try:
            self.update_feed_index()
            self.update_episodes_index()
        except:
            return 1
        return 0
    
    def dict_to_feed(self, feed_dict):
        feed = Feed(
            feed_id=feed_dict["feed_id"],
            title=feed_dict["title"],
            description=feed_dict["description"],
            link=feed_dict["link"],
            date_updated=feed_dict["date_updated"],
            feed_copyright=feed_dict["feed_copyright"]
        )
        return feed
    
    def dict_to_episode(self, episode_dict):
        episode = Episode(
            ep_id=episode_dict["ep_id"],
            feed_id=episode_dict["feed_id"],
            title=episode_dict["title"],
            description=episode_dict["description"],
            link=episode_dict["link"],
            date_added=episode_dict["date_added"],
            ep_copyright=episode_dict["ep_copyright"],
            source_url=episode_dict["source_url"]
        )
        return episode
    
    def add_podcast(self, url):
        try:
            feed_dict, episodes_dict = XmlFeed(url=url).parse()
        except:
            return 1

        feed = self.dict_to_feed(feed_dict)
        episodes = []
        for episode_dict in episodes_dict:
            episodes.append(self.dict_to_episode(episode_dict))

        self.data_index.feeds.items.append(feed)
        self.data_index.episodes.items.extend(episodes)
        return self.update_indexes()
    
    def delete_podcast(self, feed_id):
        self.data_index.feeds.items = [i for i in self.data_index.feeds.items if i.feed_id != feed_id]
        self.data_index.episodes.items = [i for i in self.data_index.episodes.items if i.feed_id != feed_id]
        return self.update_indexes()
    
    def load(self):
        debug_print("Reading JSON indexes...")
        feeds_index_dict = self.read_feeds_index()
        if feeds_index_dict is None:
            feeds_index_dict = []
        episodes_index_dict = self.read_episodes_index()
        if episodes_index_dict is None:
            episodes_index_dict = []

        if feeds_index_dict is not None and episodes_index_dict is not None:
            debug_print("Converting indexes...")
            feeds_index = FeedsIndex(feeds_index_dict)
            episodes_index = EpisodesIndex(episodes_index_dict)
            self.data_index = DataIndex(feeds_index, episodes_index)
        else:
            print("Error: Unable to read indexes!")
            return 1
        return 0

    def main(self):
        self.load()


if __name__ == "__main__":
    Podzol().main()
