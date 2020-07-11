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
    
    def as_dict(self):
        items_dict = []
        for item in self.items:
            item_dict = item.as_dict()
            items_dict.append(item_dict)
        return items_dict

    def list(self):
        for feed in self.items:
            feed.contents()
