import cv2
import threading

class CountsPerSec:
    def __init__(self):
        self._count = 0
        self._start_time = 0

    def start(self):
        self._count = 0
        self._start_time = cv2.getTickCount()
        return self

    def increment(self):
        self._count += 1

    def countsPerSec(self):
        elapsed_time = (cv2.getTickCount() - self._start_time) / cv2.getTickFrequency()
        if elapsed_time > 0:
            return self._count / elapsed_time
        else:
            return 0

class VideoGet:
    def __init__(self, source=0):
        self._source = source
        self._video_stream = None
        self._stopped = False
        self._frame = None
        self._lock = threading.Lock()

    def start(self):
        self._video_stream = cv2.VideoCapture(self._source)
        self._stopped = False
        self._frame = None
        thread = threading.Thread(target=self._get)
        thread.start()
        return self

    def stop(self):
        self._stopped = True

    def _get(self):
        while not self._stopped:
            grabbed, frame = self._video_stream.read()
            if not grabbed:
                self.stop()
            else:
                with self._lock:
                    self._frame = frame

    @property
    def frame(self):
        with self._lock:
            return self._frame

    @property
    def stopped(self):
        return self._stopped

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
                (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def showVideo(source=0):
    """Grab and show video frames without multithreading."""
    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()

    while True:
        grabbed, frame = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()

    cap.release()
    cv2.destroyAllWindows()

def main():
    video_getter = VideoGet().start()
    cps = CountsPerSec().start()

    while True:
        frame = video_getter.frame
        if frame is None or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()

    video_getter.stop()
cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


    ######

    """def noThreading(source=0):
    #Grab and show video frames without multithreading.

    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()

    while True:
        grabbed, frame = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()
    


def threadVideoGet(source=0):
    
    #Dedicated thread for grabbing video frames with VideoGet object.
    #Main thread shows video frames.
    

    video_getter = VideoGet(source).start()
    cps = CountsPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()
    cv2.destroyAllWindows()


def main():
    threadVideoGet()

if __name__ == "__main__":
    main()


def threadVideoShow(source=0):
    
    #Dedicated thread for showing video frames with VideoShow object.
    #Main thread grabs video frames.

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()
    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()"""
    
    