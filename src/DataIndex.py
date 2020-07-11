class DataIndex(object):
    def __init__(self, feeds, episodes):
        self.feeds = feeds
        self.episodes = episodes
    
    def contains_keyword(self, keywords, search_vector):
        for keyword in keywords:
            if keyword.lower() in search_vector.lower():
                return True
            return False
    
    def search(self, keywords=[], search_feeds=True, search_episodes=True):
        results = {
            "feeds": [],
            "episodes": []
        }
        if search_feeds is True:
            for feed in self.feeds.items:
                if self.contains_keyword(keywords, feed.title) is True:
                    results["feeds"].append(feed)
                elif self.contains_keyword(keywords, feed.description) is True:
                    results["feeds"].append(feed)
        if search_episodes is True:
            for episode in self.episodes.items:
                if self.contains_keyword(keywords, episode.title) is True:
                    results["episodes"].append(episode)
                elif self.contains_keyword(keywords, episode.description) is True:
                    results["episodes"].append(episode)
        return results
