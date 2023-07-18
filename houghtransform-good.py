import numpy as np
import cv2 as cv
#import streamlit as st
#cap = cv.VideoCapture(0)
#object_detector = cv.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
'''MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
DP = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
Param1 = st.sidebar.slider("Parameter 1", 1, 200, 1)
Param2 = st.sidebar.slider("Parameter 2", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)'''
img = cv.imread('/Users/josephtemplet/Desktop/work/housing2.jpg')
'''while True:
    if video.isOpened():
        ret, frame = cap.read()
    if not ret: break
    img = cv.imread('frame', cv.IMREAD_COLOR)
    mask = object_detector.apply(frame)'''
#if (cap.isOpened()== False): 
    #print("Error opening video stream or file")
   
while(True):
  # Capture frame-by-frame
    #ret, frame = cap.read()
    
        #img = cv.imread('frame', cv.IMREAD_COLOR) 

    img = cv.imread('/Users/josephtemplet/Desktop/work/housing2.jpg')
    if img is None:
        break
    output = img.copy()
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(blur, 
    cv.HOUGH_GRADIENT, minDist=100,
                           dp=1.2,
                           param1=130,
                           param2=40,
                           minRadius=0,
                           maxRadius=40)
    if circles is not None:
        detected_circles = np.uint16(np.around(circles))
        for (x, y ,r) in detected_circles[0, :]:
            cv.circle(img, (x, y), r, (0, 0, 0), 3)
            cv.circle(img, (x, y), 2, (0, 255, 255), 3)

    

    '''output = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(blur, 
        cv.HOUGH_GRADIENT, minDist=MinDist,
                           dp=DP,
                           param1=Param1,
                           param2=Param2,
                           minRadius=MinRadius,
                           maxRadius=MaxRadius) '''



    cv.imshow('img',img)
    #st.image("output", output)
    k = cv.waitKey(0) & 0xFF
    if k == ord('c'): #you can put any key here
        break
#cap.release()
cv.destroyAllWindows()

