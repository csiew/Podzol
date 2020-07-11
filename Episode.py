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
