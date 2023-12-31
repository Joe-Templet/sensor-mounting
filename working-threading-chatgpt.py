#from queue import Queue
# #from stframe import st_frame
import streamlit as st
import cv2 
import multiprocessing as mp
from multiprocessing import Queue
import numpy as np
from kthread import KThread
#from CountsPerSec import CountsPerSec


object_detector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
dp = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
max_canny_threshold = st.sidebar.slider("Canny Threshold", 1, 200, 1)
marker_threshold = st.sidebar.slider("Marker Threshold", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
detect_edges = st.sidebar.checkbox("show edge detection")
show_circles = st.sidebar.checkbox("show radius limits")

    #def putIterationsPerSec(frame, iterations_per_sec):
    
        #Add iterations per second text to lower-left corner of a frame.
    

        #cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
        #return frame
        # 

    

        
def display_webcam():
    #cps = CountsPerSec().start()
    cap = cv2.VideoCapture(0)
    while True:
       
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from the webcam")
            break
        #frame = putIterationsPerSec(frame, cps.countsPerSec())
        mask = object_detector.apply(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(blur, 
            cv2.HOUGH_GRADIENT, minDist=MinDist,
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

        yield frame

   

if __name__ == '__main__':
  
    # Create a separate process for displaying the webcam feed
    process = mp.Process(target=display_webcam)
    #grab = mp.Process(target=capture, args=(q,))

    # Start the process
    #grab.start()
    process.start()

    # Create a placeholder for displaying the video frame
    frame_placeholder = st.empty()
    stop_button = st.button("Stop Webcam")
    # Continuously update the vdeo frame in the Streamlit app
    #while True:
        #frame = display_webcam(q).__next__()
    for frame in display_webcam():
        frame_placeholder.image(frame, channels="BGR")

        # Check if the 'q' key is pressed to stop the program
        if stop_button:
            break

    # Terminate the process
    #grab.terminate()
    process.terminate()
