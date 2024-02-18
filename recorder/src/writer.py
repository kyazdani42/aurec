from video import Frame, VideoWriter

class Writer():
    def __init__(self):
        self.writer = None

    def init(self, filename: str, frame: Frame):
        self.writer = VideoWriter()
        h, w = frame.shape[:2]
        self.writer.open(filename, 14.5, (w, h))

    def release(self):
        self.writer = None

    def write(self, filename: str, frame: Frame):
        if self.writer is None:
            self.init(filename, frame)
        self.writer.write(frame) # type:ignore
