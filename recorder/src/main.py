from time import sleep

from video import Frame

from timer import Timer
from writer import Writer
from camera import Camera
from stream import Stream
from recorder import Recorder

from compare_frames import compare_frames

def start_recording(stream: Stream, recorder: Recorder, frame: Frame):
    on_start = lambda fname: stream.send_message("rec_start", fname)
    on_end = lambda fname: stream.send_message("rec_end", fname)
    recorder.start(frame, on_start, on_end)

def execute(stream: Stream, recorder: Recorder, current_frame: Frame, previous_frame: Frame):
    stream.send_frame(current_frame)
    is_recording = recorder.is_recording()
    is_moving = compare_frames(previous_frame, current_frame)

    if is_moving and not is_recording:
        try:
            start_recording(stream, recorder, current_frame)
        except Exception as e:
            print('[RECORDER]', e)
    elif is_recording:
        recorder.record(current_frame, is_moving)

def get_frame_or_exit(frame: Frame | None) -> Frame:
    if frame is None:
        print("Could not read video stream")
        exit(1)
    else:
        return frame

def run(camera: Camera, stream: Stream, recorder: Recorder):
    previous_frame = get_frame_or_exit(camera.get_frame())
    while True:
        sleep(60 / 1000)
        current_frame = get_frame_or_exit(camera.get_frame())
        execute(stream, recorder, current_frame, previous_frame)
        previous_frame = current_frame

def main():
    run(Camera(), Stream(), Recorder(Timer(), Writer()))

if __name__ == '__main__':
    main()
