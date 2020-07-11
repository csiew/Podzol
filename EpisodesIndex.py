from Episode import Episode


class EpisodesIndex(object):
    def __init__(self, episodes_index_dict):
        self.episodes_index_dict = episodes_index_dict
        self.episodes = []
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
            self.episodes.append(converted_episode)

    def list(self):
        print(self.episodes)
