import numpy as np
import cv2 as cv
import streamlit as st
from queue import Queue
from threading import Thread

from vidcap_class import vidcap
class Player:
    def __init__(self):
        self.has_loop = False
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("should close thread")
        if self.display_video:
            self.t1.terminate()


    #cap = cv.VideoCapture(0)
    #object_detector = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
    
    def __enter__(self):
        with st.sidebar:
            self.object_detector = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
            self.MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
            self.DP = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
            self.max_canny_threshold = st.sidebar.slider("Max Canny Threshhold", 1, 200, 1)
            self.marker_threshold = st.sidebar.slider("Marker Threshold", 1, 200, 1)
            self.MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
            self.MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
            self.detect_edges = st.checkbox("show edge detection")
            self.show_circles = st.checkbox("show radius limits")
            self.display_video = st.checkbox("video")
            if self.display_video:
                self.q = Queue()
                self.t1 = Thread(target = vidcap, args =(self.q, ))
                self.image = st.empty()
    def loop(self):
        if self.display_video:
            frame = self.q.get()
            self.q.queue.clear()
            self.mask = self.object_detector.apply(frame)
            gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
            blur = cv.medianBlur(gray, 5)
            self.circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 
                        minDist=self.MinDist,
                        dp=self.DP,
                        param1=self.max_canny_threshold,
                        param2=self.marker_threshold,
                        minRadius=self.MinRadius,
                        maxRadius=self.MaxRadius)
            if self.circles is not None:
                detected_circles = np.uint16(np.around(self.circles))
                for (x, y ,r) in detected_circles[0, :]:
                    cv.circle(frame, (x, y), r, (0, 0, 0), 3)
                    cv.circle(frame, (x, y), 2, (0, 255, 255), 3)    
            if self.detect_edges:
                frame = cv.Canny(frame,self.max_canny_threshold/2,self.max_canny_threshold)
            if self.show_circles:
                cv.circle(frame, (100,100), self.MinRadius, (0, 100, 100), 3)
                cv.circle(frame, (100,100), self.MaxRadius, (0, 100, 100), 3)
      
       
    
 
    
    
    #cv.imshow('frame',frame)
    #st.image('frame',frame)

            self.image.image(frame)




#circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, minDist=MinDist,
                           #dp=DP,
                           #param1=Param1,
                           #param2=Param2,
                           #minRadius=MinRadius,
                           #maxRadius=MaxRadius) 
#circles = cv.HoughCircles(blur, 
#cv.HOUGH_GRADIENT, minDist=100,
                           #dp=1.2,
                           #param1=130,
                           #param2=40,
                           #minRadius=0,
                           #maxRadius=40)
