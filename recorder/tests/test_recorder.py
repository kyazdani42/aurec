import unittest

from unittest.mock import MagicMock
from numpy import ndarray

from src.recorder import Recorder

class RecorderTester():
    def __init__(self, timer_start: float = 0.0):
        self.TimerMock = MagicMock()
        self.TimerMock.get_time.return_value = timer_start
        self.FileWriterMock = MagicMock()
        self.recorder = Recorder(self.TimerMock, self.FileWriterMock)

    def start(self):
        data = ndarray(1)
        on_start_mock = MagicMock()
        on_end_mock = MagicMock()
        self.recorder.start(data, on_start_mock, on_end_mock)
        return data, on_start_mock, on_end_mock

    def record(self, after: float = 0.0, reset: bool = False):
        if after != 0.0:
            self.TimerMock.get_time.return_value = after
        self.recorder.record(ndarray(1), reset)

class TestRecorder(unittest.TestCase):
    def test_stop_recording_after_timer_expired(self):
        R = RecorderTester()
        R.start()
        R.record(after=30.0)
        self.assertFalse(R.recorder.is_recording())

    def test_continue_recording_before_timer_expires(self):
        R = RecorderTester()
        R.start()
        R.record(after=27.0)
        self.assertTrue(R.recorder.is_recording())

    def test_continue_recording_after_timer_reset(self):
        R = RecorderTester()
        R.start()
        R.record(after=31.0, reset=True)
        self.assertTrue(R.recorder.is_recording())

    def test_calls_on_start_with_filename_when_starting(self):
        R = RecorderTester()
        _, on_start_mock, _ = R.start()
        on_start_mock.assert_called()

    def test_calls_on_end_once_when_recording_is_done(self):
        R = RecorderTester()
        _, _, on_end_mock = R.start()
        R.record(after=31.0)
        on_end_mock.assert_called()

    def test_release_writer_on_end(self):
        R = RecorderTester()
        R.start()
        R.record(after=31.0)
        R.FileWriterMock.release.assert_called()

    def test_writes_frame_to_the_file_when_recording_starts(self):
        R = RecorderTester()
        data, _, _ = R.start()
        R.FileWriterMock.write.assert_called_with("rec-01-01-1970.00:00:00", data)

    def test_filename_properly_formatted_when_recording_starts(self):
        R = RecorderTester(timer_start=61.0)
        data, _, _ = R.start()
        R.FileWriterMock.write.assert_called_with("rec-01-01-1970.00:01:01", data)

    def test_writer_fails_to_write_throws_and_doesnt_record(self):
        R = RecorderTester()
        ex = Exception("test")
        R.FileWriterMock.write.side_effect = ex
        try:
            R.start()
        except Exception as e:
            self.assertIs(e, ex)
        self.assertFalse(R.recorder.is_recording())

if __name__ == '__main__':
    unittest.main()
