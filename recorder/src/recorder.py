from typing import Callable
from datetime import datetime

from video import Frame
from timer import Timer
from writer import Writer

FnStrNone = Callable[[str], None]
FnFloat = Callable[[], float]

FileWriter = {}

def format_date(n: float) -> str:
    dt = datetime.utcfromtimestamp(n)
    return dt.strftime("rec-%d-%m-%Y.%H:%M:%S")

class Recorder():
    def __init__(self, timer: Timer, writer: Writer):
        self.Timer = timer
        self.Writer = writer
        self._reset_state()

    def _reset_state(self):
        self._record_started_at = None
        self._filename = None
        self._on_end = None

    def is_recording(self):
        return self._filename is not None

    # this method should only be used when self.is_recording() is false
    def start(self, frame: Frame, on_start: FnStrNone, on_end: FnStrNone):
        self._record_started_at = self.Timer.get_time()
        self._filename = format_date(self._record_started_at)
        try:
            self.Writer.write(self._filename, frame)
            on_start(self._filename)
            self._on_end = on_end
        except Exception as e:
            self._reset_state()
            raise e

    # ignoring types to let method crash the process when used inappropriately
    # this method should only be used when self.is_recording() is true
    def record(self, frame: Frame, reset: bool):
        self.Writer.write(self._filename, frame) # type: ignore
        time = self.Timer.get_time()
        if reset:
            self._record_started_at = time
        elif time - self._record_started_at > 29: # type: ignore
            self._on_end(self._filename) # type: ignore
            self.Writer.release()
            self._reset_state()
