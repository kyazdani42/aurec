import cv2
from os import environ as env

from video import Frame

STORAGE_FOLDER = env.get("AUREC_VIDEO_LOCATION") or "/tmp"
CODEC = cv2.VideoWriter.fourcc(*'mp4v')

class Writer():
    def __init__(self):
        self.writers = {}

    def init(self, filename: str, frame: Frame):
        self.writers[filename] = cv2.VideoWriter()
        self._filename = STORAGE_FOLDER + "/" + filename + ".mp4"
        h, w = frame.shape[:2]
        self.writers[filename].open(self._filename, CODEC, 14.5, (w, h), True)

    def release(self, filename: str):
        self.writers[filename].release()
        self.writers.pop(filename)

    def write(self, filename: str, frame: Frame):
        if not self.writers.get(filename):
            self.init(filename, frame)

        if not self.writers[filename].isOpened():
            raise Exception("Failed to write to file " + self._filename)
        else:
            self.writers[filename].write(frame)
