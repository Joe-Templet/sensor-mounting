#import argparse
import time
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow
import streamlit as st
import numpy as np
from queue import Queue

def putIterationsPerSec(frame, iterations_per_sec):
    
    #Add iterations per second text to lower-left corner of a frame.
    

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
                (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame


def threadBoth(source=0):
    #Dedicated thread for grabbing video frames with VideoGet object.
    #Dedicated thread for showing video frames with VideoShow object.
    #Main thread serves only to pass frames between VideoGet and
    #VideoShow objects/threads.
    object_detector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
    MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
    dp = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
    max_canny_threshold = st.sidebar.slider("Parameter 1", 1, 200, 1)
    marker_threshold = st.sidebar.slider("Parameter 2", 1, 200, 1)
    MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
    MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
    detect_edges = st.sidebar.checkbox("show edge detection")
    display_video = st.sidebar.checkbox("display video")
    show_circles = st.sidebar.checkbox("show radius limits")
    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()
    while True:
        if display_video:
            frame = video_getter.frame
            #frame = putIterationsPerSec(frame, cps.countsPerSec())
        
            mask = object_detector.apply(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 5)
            circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
                minDist=MinDist,
                dp=dp,
                param1=max_canny_threshold,
                param2=marker_threshold,
                minRadius=MinRadius,
                maxRadius=MaxRadius)
    
            if circles is not None:
                detected_circles = np.uint16(np.around(circles))
                for (x, y, r) in detected_circles[0, :]:       
                    cv2.circle(frame, (x, y), r, (0, 0, 0), 3)
                    cv2.circle(frame, (x, y), 2, (0, 255, 255), 3)

            if detect_edges:
                frame = cv2.Canny(frame, max_canny_threshold/2, max_canny_threshold)
        
            if show_circles:
                cv2.circle(frame, (100, 100), MinRadius, (0, 100, 100), 3)
                cv2.circle(frame, (100, 100), MaxRadius, (0, 100, 100), 3)
##         
        
        
            video_shower.frame = frame
            cps.increment()
    video_shower.stop()
    video_getter.stop()
    cv2.destroyAllWindows()

def main():
    threadBoth()

if __name__ == "__main__":
    main()

## 7/17 -Stopping point: havent tested anything qith queue. Try to have the images collect ina queue. Set up GitHub. 
