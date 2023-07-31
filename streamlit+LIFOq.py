#from queue import Queue
# #from stframe import st_frame
import streamlit as st
import cv2 
import multiprocessing as mp
from multiprocessing import Manager
from queue import LifoQueue 
from queue import Queue
import numpy as np
import time
from threading import Thread
from kthread import KThread



object_detector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
dp = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
max_canny_threshold = st.sidebar.slider("canny threshold", 1, 200, 1)
marker_threshold = st.sidebar.slider("marker_threshold", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
detect_edges = st.sidebar.checkbox("show edge detection")
show_circles = st.sidebar.checkbox("show radius limits")
stop_button = st.sidebar.button('STOP')

    
def capture(q):
    cap = cv2.VideoCapture(0)
    while True:
        
        ret, f1 = cap.read()
        q.put(f1)
    
        if not ret:
            print("Failed to capture frame from the webcam") 
    cap.release()
    

        
def display_webcam(q):
    #cps = CountsPerSec().start()
    while True:
        #frame = putIterationsPerSec(frame, cps.countsPerSec())
        frame = q.get()
        mask = object_detector.apply(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(blur, 
        cv2.HOUGH_GRADIENT, minDist=190,
        dp=120,
        param1=150,
        param2=50,
        minRadius=50,
        maxRadius=160)

        if circles is not None:
            detected_circles = np.uint16(np.around(circles))
            for (x, y, r) in detected_circles[0, :]:       
                cv2.circle(frame, (x, y), r, (0, 0, 0), 3)
                cv2.circle(frame, (x, y), 2, (0, 255, 255), 3)
        #cv2.imshow("Processed Frame", frame)
        #if cv2.waitKey(1) & 0xFF == ord('e'):
            #break
        if detect_edges:
            frame = cv2.Canny(frame, max_canny_threshold/2, max_canny_threshold)
        
        if show_circles:
            cv2.circle(frame, (100, 100), MinRadius, (0, 100, 100), 3)
            cv2.circle(frame, (100, 100), MaxRadius, (0, 100, 100), 3)
        
        yield frame
        #cv2.imshow('Frame', frame)
        #if cv2.waitKey(1) & 0xFF == ord('w'):
            #print(cap_count.value - proc_count.value)
            #break

   

if __name__ == '__main__':

    q=LifoQueue()
    grab = KThread(target=capture, args=(q, ))
    # Start the process
    grab.start()
    display_webcam(q)
   
    # Create a placeholder for displaying the video frame
    frame_placeholder = st.empty()
    stop_button = st.button("Stop Webcam")
    # Continuously update the vdeo frame in the Streamlit app
    frame_placeholder = st.empty()
    for frame in display_webcam(q):
        frame_placeholder.image(frame, channels="BGR")
            # Check if the 'q' key is pressed to stop the program
        if stop_button:
            break
    # Terminate the process
    
    grab.join()
    #process.terminate()
    cv2.destroyAllWindows()
    