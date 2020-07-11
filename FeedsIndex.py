from Feed import Feed


class FeedsIndex(object):
    def __init__(self, feeds_index_dict):
        self.feeds_index_dict = feeds_index_dict
        self.items = []
        self.convert()

    def convert(self):
        for feed in self.feeds_index_dict:
            converted_feed = Feed(
                feed_id=feed["feed_id"],
                title=feed["title"],
                description=feed["description"],
                link=feed["link"],
                date_updated=feed["date_updated"],
                feed_copyright=feed["feed_copyright"]
            )
            self.items.append(converted_feed)

    def list(self):
        for feed in self.items:
            feed.contents()
