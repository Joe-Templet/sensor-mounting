import numpy as np
import cv2 as cv
import streamlit as st
MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
DP = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
Param1 = st.sidebar.slider("Parameter 1", 1, 200, 1)
Param2 = st.sidebar.slider("Parameter 2", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
while True:
    img = cv.imread('/Users/josephtemplet/Desktop/work/housing2.jpg')
    if img is None:
        break

    output = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(blur, 
        cv.HOUGH_GRADIENT, minDist=MinDist,
                           dp=DP,
                           param1=Param1,
                           param2=Param2,
                           minRadius=MinRadius,
                           maxRadius=MaxRadius)
    detected_circles = np.uint16(np.around(circles))
    for (x, y ,r) in detected_circles[0, :]:
        cv.circle(output, (x, y), r, (0, 0, 0), 3)
        cv.circle(output, (x, y), 2, (0, 255, 255), 3)


    #cv.imshow('output',output)
    st.image("output", output)
    k = cv.waitKey(0) & 0xFF
    if k == ord('c'): #you can put any key here
        break
cv.destroyAllWindows()

