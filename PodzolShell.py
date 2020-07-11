from PodzolBackend import Podzol, debug_print


class PodzolShell(object):
    def __init__(self, backend):
        self.primary_commands = ["exit", "help", "list", "play"]
        self.operations = {
            "list": ["-f", "-e"]
        }
        self.shortcuts = {}
        self.backend = backend

    def index_to_shortcuts(self):
        feed_key = 0
        for feed in self.backend.data_index.feeds.items:
            self.shortcuts[feed_key] = {
                "feed": feed,
                "episodes": {}
            }
            episode_key = 0
            for episode in [ep for ep in self.backend.data_index.episodes.items if ep.feed_id == feed.feed_id]:
                self.shortcuts[feed_key]["episodes"][episode_key] = episode
                episode_key += 1
            feed_key += 1

    def list_episodes_of_feed(self, feed_key):
        print(self.shortcuts[feed_key]["feed"].title)
        for key, value in self.shortcuts[feed_key]["episodes"].items():
            print("[" + str(key) + "] - " + value.title)

    def list_feeds(self):
        for key, value in self.shortcuts.items():
            print("[" + str(key) + "] - " + value["feed"].title)

    def handle_list(self, args):
        if len(args) >= 2 and args[1] in self.operations["list"] and self.backend.data_index is not None:
            feed_key = None
            if len(args) >= 3:
                try:
                    feed_key = int(args[2])
                except:
                    print("Invalid feed key: " + args[2])
                    return
            if len(args) == 3:
                if args[1] == "-f" and feed_key in self.shortcuts.keys():
                    self.list_episodes_of_feed(feed_key)
            else:
                if len(args) < 5 and args[1] == "-f":
                    self.list_feeds()
                elif len(args) == 5 and args[3] == "-e":
                    try:
                        episode_key = int(args[4])
                    except:
                        print("Invalid episode key: " + args[4])
                        return
                    episode = self.shortcuts[feed_key]["episodes"][episode_key]
                    episode.contents()
                else:
                    print("Type 'list' to see how to use lists")
        else:
            print("list -f\t\t\t\tList all feeds")
            print("list -f [key]\t\t\tList all episodes of given feed")
            print("list -f [key] -e [key]\t\tList episode info")

    def handle_play(self, args):
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

            episode = self.shortcuts[feed_key]["episodes"][episode_key]
            debug_print(episode.source_url)
        else:
            print(usage_msg)

    def event_loop(self):
        while 1:
            command_string = input("podzol: ")
            args = command_string.split()
            if len(args) > 0 and args[0] in self.primary_commands:
                debug_print("Parsed command: " + str(args))
                if args[0] == "exit":
                    exit(0)
                elif args[0] == "help":
                    print("Commands:")
                    for item in self.primary_commands:
                        print(" " + item)
                        if item in self.operations.keys():
                            for subitem in self.operations[item]:
                                print("     " + subitem)
                elif args[0] == "list":
                    self.handle_list(args)
                elif args[0] == "play":
                    self.handle_play(args)
    
    def main(self):
        self.index_to_shortcuts()
        try:
            self.event_loop()
        except KeyboardInterrupt:
            debug_print("\nExiting Podzol...")
            exit(0)

if __name__ == "__main__":
    backend = Podzol()
    backend.main()
    PodzolShell(backend=backend).main()
