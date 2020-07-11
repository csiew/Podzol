from xml.dom import minidom
from urllib import request

episode_properties = [
    'title',
    'description',
    'link',
    'pubDate',
    'copyright'
]

feed_alias = {
    "lastBuildDate": "date_updated",
    "copyright": "feed_copyright"
}
episode_alias = {
    "pubDate": "date_added",
    "copyright": "ep_copyright"
}

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
                prop_value = self.root.getElementsByTagName(prop)[0].firstChild.nodeValue
            except:
                prop_value = "No " + prop + " specified."
                pass
            if prop in feed_alias.keys():
                self.feed[feed_alias[prop]] = prop_value
            else:
                self.feed[prop] = prop_value
        return self.feed
    
    def get_episodes(self):
        episodes = []
        items = self.root.getElementsByTagName('item')
        episode_id = len(items)
        # Always put the latest episode at the bottom
        for item in reversed(items):
            episode = {}
            for prop in episode_properties:
                try:
                    prop_value = item.getElementsByTagName(prop)[0].firstChild.nodeValue
                except:
                    prop_value = "No " + prop + " specified."
                    pass
                if prop in episode_alias.keys():
                    episode[episode_alias[prop]] = prop_value
                else:
                    episode[prop] = prop_value
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
