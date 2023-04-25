import pygame


class AudioPlayer(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def load(self, url):
        pygame.mixer.music.load(url)

    def play(self):
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def get_busy(self):
        return pygame.mixer.music.get_busy()

    def get_pos(self):
        return pygame.mixer.music.get_pos()

    def exit(self):
        pygame.exit()
