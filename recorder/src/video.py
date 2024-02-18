import os

import cv2
from cv2.typing import MatLike

Frame = MatLike

absdiff = cv2.absdiff

def threshold(frame: Frame):
    return cv2.threshold(frame, 16, 255, cv2.THRESH_BINARY) 

def to_gray(frame: Frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def find_contours(frame: Frame):
    return cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

def blur(frame: Frame):
    return cv2.GaussianBlur(frame, (21, 21), 0)

def flip180(frame: Frame):
    return cv2.flip(frame, 180)

def get_camera():
    return cv2.VideoCapture(0)

def to_binary(frame: Frame) -> bytes:
    return cv2.imencode('.jpg', frame)[1].tobytes()

_STORAGE_FOLDER = os.environ.get("AUREC_VIDEO_LOCATION") or "/tmp"
_CODEC = cv2.VideoWriter.fourcc(*'avc1')
_EXT = ".mp4"

class VideoWriter():
    def __init__(self):
        self.writer = cv2.VideoWriter()

    def __del__(self):
        self.writer.release()

    def open(self, filename: str, fps: float, wh: tuple[int, int]):
        self._filename = _STORAGE_FOLDER + "/" + filename + _EXT
        self.writer.open(self._filename, _CODEC, fps, wh)

    def write(self, frame: Frame):
        if self.writer.isOpened():
            self.writer.write(frame)
        else:
            raise Exception("Failed to write to file " + self._filename)
