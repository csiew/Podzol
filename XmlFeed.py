from xml.dom import minidom
from urllib import request

episode_properties = [
    'title',
    'description',
    'link',
    'pubDate',
    'copyright'
]

class XmlFeed(object):
    def __init__(self, url):
        self.url = url
        self.root = None
        self.feed = {
            "title": "",
            "description": "",
            "link": "",
            "lastBuildDate": "",
            "copyright": ""
        }
    
    def open_feed(self):
        error_msg = "Error: unable to open feed - " + self.url
        try:
            self.root = minidom.parse(self.url)
            return 0
        except:
            print("Not a local file... Attempting web request...")
            try:
                feed_response = request.urlopen(self.url)
                self.root = minidom.parse(feed_response)
                return 0
            except:
                print(error_msg)
        return 1
    
    def get_feed_metadata(self):
        props = [*self.feed.keys()]
        self.feed["feed_id"] = self.url
        for prop in props:
            try:
                self.feed[prop] = self.root.getElementsByTagName(prop)[0].firstChild.nodeValue
            except:
                self.feed[prop] = "No " + prop + " specified."
                pass
        return self.feed
    
    def get_episodes(self):
        episodes = []
        items = self.root.getElementsByTagName('item')
        episode_id = len(items)
        for item in items:
            episode = {}
            for prop in episode_properties:
                try:
                    prop_value = item.getElementsByTagName(prop)[0].firstChild.nodeValue
                    episode[prop] = prop_value
                except:
                    episode[prop] = "No " + prop + " specified."
                    pass
            source_url_node = item.getElementsByTagName('enclosure')
            episode["source_url"] = source_url_node[0].attributes['url'].value
            episode["ep_id"] = episode_id
            episode["feed_id"] = self.url
            episodes.append(episode)
            episode_id -= 1
        return episodes
    
    def parse(self):
        if self.open_feed() == 1:
            return 1
        feed_info = self.get_feed_metadata()
        episodes = self.get_episodes()
        return feed_info, episodes
    

if __name__ == "__main__":
    feed, episodes = XmlFeed(url="https://podcast.panic.com/index.xml").parse()
    print(feed)
    print("Episode count: " + str(len(episodes)))
    print(episodes)
