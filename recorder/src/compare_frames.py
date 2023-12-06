from video import Frame
import video

def _differentiate_frame(f1: Frame, f2: Frame) -> Frame:
    diff = video.absdiff(f1, f2)
    gray = video.to_gray(diff)
    blurred = video.blur(gray)
    _, t = video.threshold(blurred)
    return t

def _get_contours(diff: Frame):
    contours, _ = video.find_contours(diff)
    return contours

def compare_frames(frame: Frame, frame2: Frame) -> bool:
    diff = _differentiate_frame(frame, frame2)
    contours = _get_contours(diff)
    return len(contours) > 0
