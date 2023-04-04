import io
import requests
import contextlib
with contextlib.redirect_stdout(None):      # https://stackoverflow.com/a/51470016
    import pygame
import time
from PodzolBackend import Podzol, debug_print


SEPARATOR = "==========================================="


# ACKNOWLEDGEMENTS
# ResponseStream by sloth
# https://stackoverflow.com/a/58763348
class ResponseStream(object):
    def __init__(self, request_iterator):
        self._bytes = io.BytesIO()
        self._iterator = request_iterator

    def _load_all(self):
        self._bytes.seek(0, io.SEEK_END)
        for chunk in self._iterator:
            self._bytes.write(chunk)

    def _load_until(self, goal_position):
        current_position = self._bytes.seek(0, io.SEEK_END)
        while current_position < goal_position:
            try:
                current_position = self._bytes.write(next(self._iterator))
            except StopIteration:
                break

    def tell(self):
        return self._bytes.tell()

    def read(self, size=None):
        left_off_at = self._bytes.tell()
        if size is None:
            self._load_all()
        else:
            goal_position = left_off_at + size
            self._load_until(goal_position)

        self._bytes.seek(left_off_at)
        return self._bytes.read(size)

    def seek(self, position, whence=io.SEEK_SET):
        if whence == io.SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(position, whence)


class AudioPlayer(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
    
    def load(self, url):
        pygame.mixer.music.load(url)
    
    def play(self):
        pygame.mixer.music.play()
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def resume(self):
        pygame.mixer.music.unpause()
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def get_busy(self):
        return pygame.mixer.music.get_busy()
    
    def get_pos(self):
        return pygame.mixer.music.get_pos()
    
    def exit(self):
        pygame.exit()


class PodzolShell(object):
    def __init__(self, backend):
        self.primary_commands = ["exit", "help", "search", "list", "play", "add", "delete", "reload", "purge"]
        self.operations = {
            "list": ["-f", "-e"],
            "play": ["-f", "-e"],
            "delete": ["-f"],
        }
        self.podcast_index = {}
        self.backend = backend
        self.player = AudioPlayer()
    
    def audio_player(self, url):
        print("Podzol might seem unresponsive and the podcast may not play immediately due to buffering!")
        print("Finding stream...")
        response = requests.get(url, stream=True)
        print("Stream found")
        if (response.status_code == 200):
            print("Buffering stream...")
            stream = ResponseStream(response.iter_content(64))
            self.player.load(stream)
            print("Starting playback")
            self.player.play()
            print("Playing: ", url)
            while self.player.get_busy():
                timer = self.player.get_pos()
                time.sleep(1)
                print("Use the 'help' command to get a list of commands\n")
                control = input("podzol > player > ")
                pygame.time.Clock().tick(10)
                if control == "help":
                    print("[play/pause] [stop] [time] [help]")
                elif control == "pause":
                    self.player.pause()
                elif control == "play" or control == "resume" :
                    self.player.resume()
                elif control == "time":
                    timer = self.player.get_pos()
                    timer = timer/1000
                    print (str(timer))
                elif int(timer) > 10:
                    print ("Playback ended")
                    self.player.stop()
                    break
                else:
                    continue
        else:
            print("Unable to open stream")
        return

    def assemble_podcast_index(self):
        feed_key = 0
        for feed in self.backend.data_index.feeds.items:
            self.podcast_index[feed_key] = {
                "feed": feed,
                "episodes": {}
            }
            episode_key = 0
            for episode in [ep for ep in self.backend.data_index.episodes.items if ep.feed_id == feed.feed_id]:
                self.podcast_index[feed_key]["episodes"][episode_key] = episode
                episode_key += 1
            feed_key += 1

    def list_episodes_of_feed(self, feed_key):
        print(self.podcast_index[feed_key]["feed"].title)
        for key, value in self.podcast_index[feed_key]["episodes"].items():
            print("[" + str(key) + "] - " + value.title)

    def list_feeds(self):
        if len(self.podcast_index.items()) > 0:
            for key, value in self.podcast_index.items():
                print("[" + str(key) + "] - " + value["feed"].title)
        else:
            print("You don't have anything in your library")

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
                if args[1] == "-f" and feed_key in self.podcast_index.keys():
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
                    episode = self.podcast_index[feed_key]["episodes"][episode_key]
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

            episode = self.podcast_index[feed_key]["episodes"][episode_key]
            debug_print(episode.source_url)
            self.audio_player(episode.source_url)
        else:
            print(usage_msg)
    
    def get_feed_key(self, feed_id):
        for key, value in self.podcast_index.items():
            if value["feed"].feed_id == feed_id:
                return key
        return None
    
    def handle_search(self, args):
        if len(args) > 1:
            keywords = args[1:]
            results = self.backend.data_index.search(keywords)
            print("KEYWORDS: " + str(keywords))
            print("RESULTS")
            print(SEPARATOR)
            print("\tFEEDS [" + str(len(results["feeds"])) + "]:")
            for feed in results["feeds"]:
                try:
                    feed_key = self.get_feed_key(feed.feed_id)
                    print("[" + str(feed_key) + "] - " + feed.title)
                except:
                    pass
            print(SEPARATOR)
            print("\tEPISODES [" + str(len(results["episodes"])) + "]:")
            for episode in results["episodes"]:
                feed_key = self.get_feed_key(episode.feed_id)
                print("[" + str(feed_key) + "][" + str(episode.ep_id) + "] - " + episode.title)
            print(SEPARATOR)
        else:
            print("search [keyword 1] [keyword 2] [etc...]")
    
    def handle_add(self, args):
        if len(args) > 1:
            urls = args[1:]
            total = len(urls)
            success = total
            for url in urls:
                result = self.backend.add_podcast(url)
                if result == 1:
                    print("Error: Unable to add URL - " + url)
                    success -= 1
            print("Added " + str(success) + " of " + str(total) + " podcast feeds provided")
            self.assemble_podcast_index()
        else:
            print("add [url 1] [url 2] [etc...]")
    
    def handle_delete(self, args):
        usage_msg = "delete -f [key]\t\tDelete podcast and its episodes"
        if len(args) == 3:
            if not (args[1] == "-f"):
                print(usage_msg)
                return

            try:
                feed_key = int(args[2])
            except:
                print("Invalid feed key: " + args[2])
                return

            feed_id = self.podcast_index[feed_key]["feed"].feed_id
            result = self.backend.delete_podcast(feed_id)
            if result == 0:
                self.podcast_index.pop(feed_key)
                print("Removed podcast from your library: " + str(feed_id))
                self.assemble_podcast_index()
            elif result == 0:
                print("Error: Failed to update your library")
        else:
            print(usage_msg)
    
    def handle_purge(self):
        print("WARNING! This will erase your library!")
        print("Are you sure you want to continue? [Default: No]")
        user_choice = input("podzol > purge > [y/N] ")
        if user_choice.lower() == "y":
            result = self.backend.purge()
            if result == 0:
                print("Library purged")
            else:
                print("Error: Unable to purge library")
        else:
            print("Not purging library")

    def handle_reload(self):
        print("Reloading indexes...")
        self.backend.load()
        self.assemble_podcast_index()
    
    def handle_help(self):
        print("Commands:")
        for item in self.primary_commands:
            print(" - " + item)
            if item in self.operations.keys():
                for subitem in self.operations[item]:
                    print("     " + subitem)

    def event_loop(self):
        print("Podzol: A minimalist CLI podcast client")
        print("Use the 'help' command to get a list of commands\n")
        while 1:
            command_string = input("podzol > ")
            args = command_string.split()
            if len(args) > 0 and args[0] in self.primary_commands:
                debug_print("Parsed command: " + str(args))
                if args[0] == "exit":
                    exit(0)
                elif args[0] == "help":
                    self.handle_help()
                elif args[0] == "search":
                    self.handle_search(args)
                elif args[0] == "list":
                    self.handle_list(args)
                elif args[0] == "play":
                    self.handle_play(args)
                elif args[0] == "add":
                    self.handle_add(args)
                elif args[0] == "delete":
                    self.handle_delete(args)
                elif args[0] == "purge":
                    self.handle_purge()
                elif args[0] == "reload":
                    self.handle_reload()
                else:
                    continue
    
    def main(self):
        self.assemble_podcast_index()
        try:
            self.event_loop()
        except KeyboardInterrupt:
            debug_print("\nExiting Podzol...")
            exit(0)

if __name__ == "__main__":
    backend = Podzol()
    backend.main()
    PodzolShell(backend=backend).main()
