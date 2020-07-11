class Episode(object):
    def __init__(self, ep_id, feed_id, title, description, link, date_added, ep_copyright, source_url):
        self.ep_id = ep_id
        self.feed_id = feed_id
        self.title = title
        self.description = description
        self.link = link
        self.date_added = date_added
        self.ep_copyright = ep_copyright
        self.source_url = source_url
    
    def as_dict(self):
        episode_dict = {
            "ep_id": self.ep_id,
            "feed_id": self.feed_id,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "date_added": self.date_added,
            "ep_copyright": self.ep_copyright,
            "source_url": self.source_url
        }
        return episode_dict

    def contents(self):
        print("id:\t\t\t" + self.ep_id)
        print("feed_id:\t\t" + self.feed_id)
        print("title:\t\t\t" + self.title)
        print("description:\t\t" + self.description)
        print("link:\t\t\t" + self.link)
        print("date_added:\t\t" + self.date_added)
        print("ep_copyright:\t\t" + self.ep_copyright)
        print("source_url:\t\t" + self.source_url)
        print("\n")
