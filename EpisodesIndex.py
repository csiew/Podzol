from Episode import Episode


class EpisodesIndex(object):
    def __init__(self, episodes_index_dict):
        self.episodes_index_dict = episodes_index_dict
        self.items = []
        self.convert()

    def convert(self):
        for episode in self.episodes_index_dict:
            converted_episode = Episode(
                ep_id=episode["ep_id"],
                feed_id=episode["feed_id"],
                title=episode["title"],
                description=episode["description"],
                link=episode["link"],
                date_added=episode["date_added"],
                ep_copyright=episode["ep_copyright"],
                source_url=episode["source_url"]
            )
            self.items.append(converted_episode)
    
    def as_dict(self):
        items_dict = []
        for item in self.items:
            item_dict = item.as_dict()
            items_dict.append(item_dict)
        return items_dict

    def list(self):
        for episode in self.items:
            episode.contents()
