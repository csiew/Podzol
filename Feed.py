class Feed(object):
    def __init__(self, feed_id, title, description, link, date_updated, feed_copyright):
        self.feed_id = feed_id
        self.title = title
        self.description = description
        self.link = link
        self.date_updated = date_updated
        self.feed_copyright = feed_copyright

    def contents(self):
        print("id:\t\t\t" + self.feed_id)
        print("title:\t\t\t" + self.title)
        print("description:\t\t" + self.description)
        print("link:\t\t\t" + self.link)
        print("date_updated:\t\t" + self.date_updated)
        print("feed_copyright:\t\t" + self.feed_copyright)
        print("\n")
