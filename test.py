import pygame
import requests
import urllib.request
import io
import time

class ResponseStream(object):
    def __init__(self, request_iterator):
        self._bytes = io.BytesIO()
        self._iterator = request_iterator

    def _load_all(self):
        self._bytes.seek(0, io.SEEK_END)
        for chunk in self._iterator:
            self._bytes.write(chunk)

    def _load_until(self, goal_position):
        current_position = self._bytes.seek(0, io.SEEK_END)
        while current_position < goal_position:
            try:
                current_position = self._bytes.write(next(self._iterator))
            except StopIteration:
                break

    def tell(self):
        return self._bytes.tell()

    def read(self, size=None):
        left_off_at = self._bytes.tell()
        if size is None:
            self._load_all()
        else:
            goal_position = left_off_at + size
            self._load_until(goal_position)

        self._bytes.seek(left_off_at)
        return self._bytes.read(size)

    def seek(self, position, whence=io.SEEK_SET):
        if whence == io.SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(position, whence)


files = ['https://anchor.fm/s/10256858/podcast/play/14887303/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fproduction%2F2020-5-8%2F80428201-44100-2-3172e09cabb34.mp3']
pygame.init()
pygame.mixer.init()
stepper = 0
#file loading
while stepper < len(files):
    response = requests.get(files[stepper], stream=True)
    if (response.status_code == 200):
        stream = ResponseStream(response.iter_content(64))
        pygame.mixer.music.load(stream)
        pygame.mixer.music.play()
        print("Playing:",files[stepper])
        stepper += 1
        #play and pause
        while pygame.mixer.music.get_busy():
            timer = pygame.mixer.music.get_pos()
            time.sleep(1)
            control = input()
            pygame.time.Clock().tick(10)
            if control == "pause":
                pygame.mixer.music.pause()
            elif control == "play" :
                pygame.mixer.music.unpause()
            elif control == "time":
                timer = pygame.mixer.music.get_pos()
                timer = timer/1000
                print (str(timer))
            elif int(timer) > 10:
                print ("True")
                pygame.mixer.music.stop()
                break
            else:
                continue
    else:
        print("Unable to open stream")
pygame.quit()
