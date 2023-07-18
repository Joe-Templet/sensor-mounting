import numpy as np
import cv2 as cv
import streamlit as st
from queue import Queue
from threading import Thread
class Vidcap:
    def __init__(self,src=0):
        self.cap = cv.VideoCapture(src)
        (self.ret, self.frame) = self.cap.read()
        self.stopped = False
    def start(self):
		# start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
    def update(self):
		# keep looping infinitely until the thread is stopped
        while True:
			# if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
			# otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.cap.read()
    def read(self):
		# return the frame most recently read
        return self.frame
    def stop(self):
		# indicate that the thread should be stopped
        self.stopped = True
        self.cap.release()
    while True:
        k = cv.waitKey(1) & 0xFF
        if k == ord('c'): #you can put any key here
            break
        
cv.destroyAllWindows()