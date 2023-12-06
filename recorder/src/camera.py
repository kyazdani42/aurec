import video

class Camera():
    def __init__(self):
        self._camera = video.get_camera()

    def __del__(self):
        self._camera.release()

    def get_frame(self):
        ret, frame = self._camera.read()
        if not ret:
            return None
        return video.flip180(frame)
