from xml.dom import minidom

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
        self.root = minidom.parse(url)
        self.feed = {
            "title": "",
            "description": "",
            "link": "",
            "feed_copyright": ""
        }
        self.episodes = []
    
    def get_feed_info(self):
        self.feed["title"] = self.root.getElementsByTagName('title')
        self.feed["description"] = self.root.getElementsByTagName('description')
        self.feed["link"] = self.root.getElementsByTagName('link')
        self.feed["feed_copyright"] = self.root.getElementsByTagName('copyright')
        print(self.feed)
    
    def get_episodes(self):
        items = self.root.getElementsByTagName('item')
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
            print(episode)
            self.episodes.append(episode)
    

if __name__ == "__main__":
    xmlfeed = XmlFeed(url="data/takeaway_table.xml")
    xmlfeed.get_episodes()
