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
        primary_commands = ["exit", "help", "list", "play"]
        operations = {
            "list": ["-f", "-e"]
        }
        shortcuts = {}

        def index_to_shortcuts():
            feed_key = 0
            for feed in self.data_index.feeds.items:
                shortcuts[feed_key] = {
                    "feed": feed,
                    "episodes": {}
                }
                episode_key = 0
                for episode in [ep for ep in self.data_index.episodes.items if ep.feed_id == feed.feed_id]:
                    shortcuts[feed_key]["episodes"][episode_key] = episode
                feed_key += 1

        def list_episodes_of_feed(feed_key):
            print(shortcuts[feed_key]["feed"].title)
            for key, value in shortcuts[feed_key]["episodes"].items():
                print("[" + str(key) + "] - " + value.title)

        def list_feeds():
            for key, value in shortcuts.items():
                print("[" + str(key) + "] - " + value["feed"].title)

        def handle_list(args):
            if len(args) >= 2 and args[1] in operations["list"] and self.data_index is not None:
                feed_key = None
                if len(args) >= 3:
                    try:
                        feed_key = int(args[2])
                    except:
                        print("Invalid feed key: " + args[2])
                        return
                if len(args) == 3:
                    if args[1] == "-f" and feed_key in shortcuts.keys():
                        list_episodes_of_feed(feed_key)
                else:
                    if len(args) < 5 and args[1] == "-f":
                        list_feeds()
                    elif len(args) == 5 and args[3] == "-e":
                        try:
                            episode_key = int(args[4])
                        except:
                            print("Invalid episode key: " + args[4])
                            return
                        episode = shortcuts[feed_key]["episodes"][episode_key]
                        episode.contents()
                    else:
                        print("Type 'list' to see how to use lists")
            else:
                print("list -f\t\t\t\tList all feeds")
                print("list -f [key]\t\t\tList all episodes of given feed")
                print("list -f [key] -e [key]\t\tList episode info")

        def handle_play(args):
            usage_msg = "play -f [key] -e [key]\t\tPlay episode"
            if len(args) == 5:
                if not (args[1] == "-f" and args[3] == "-e"):
                    print(usage_msg)
                    return

                try:
                    feed_key = int(args[2])
                except:
                    print("Invalid feed key: " + args[2])
                    return

                try:
                    episode_key = int(args[4])
                except:
                    print("Invalid episode key: " + args[4])
                    return

                episode = shortcuts[feed_key]["episodes"][episode_key]
                print(episode.source_url)
            else:
                print(usage_msg)

        index_to_shortcuts()
        while 1:
            command_string = input("podzol: ")
            args = command_string.split()
            if len(args) > 0 and args[0] in primary_commands:
                debug_print("Parsed command: " + str(args))
                if args[0] == "exit":
                    exit(0)
                elif args[0] == "help":
                    print("Commands:")
                    for item in primary_commands:
                        print(" " + item)
                        if item in operations.keys():
                            for subitem in operations[item]:
                                print("     " + subitem)
                elif args[0] == "list":
                    handle_list(args)
                elif args[0] == "play":
                    handle_play(args)

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
