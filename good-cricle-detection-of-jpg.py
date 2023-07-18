import numpy as np
import cv2 as cv
import streamlit as st
cap = cv.VideoCapture(0)
object_detector = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
DP = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
max_canny_threshold = st.sidebar.slider("Parameter 1", 1, 200, 1)
marker_threshold = st.sidebar.slider("Parameter 2", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
detect_edges = st.checkbox("show edge detection")
show_circles = st.checkbox("show radius limits")
image=st.empty()
#img = cv.imread('/Users/josephtemplet/Desktop/work/housing2.jpg')
while True:
   
    ret, frame = cap.read()
   
    
    mask = object_detector.apply(frame)
#if (cap.isOpened()== False): 
    #print("Error opening video stream or file")
   
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(blur, 
    cv.HOUGH_GRADIENT, minDist=MinDist,
                           dp=DP,
                           param1=max_canny_threshold,
                           param2=marker_threshold,
                           minRadius=MinRadius,
                           maxRadius=MaxRadius)
    if circles is not None:
        detected_circles = np.uint16(np.around(circles))
        for (x, y ,r) in detected_circles[0, :]:
            cv.circle(frame, (x, y), r, (0, 0, 0), 3)
            cv.circle(frame, (x, y), 2, (0, 255, 255), 3)

    if detect_edges:
                frame = cv.Canny(frame,max_canny_threshold/2,max_canny_threshold)
    if show_circles:
                cv.circle(frame, (100,100), MinRadius, (0, 100, 100), 3)
                cv.circle(frame, (100,100), MaxRadius, (0, 100, 100), 3)

    



    #cv.imshow('img',img)
    image.image(frame)
    k = cv.waitKey(1) & 0xFF
    if k == ord('c'): #you can put any key here
        break
cap.release()
cv.destroyAllWindows()

