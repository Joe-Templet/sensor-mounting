import numpy as np
import argparse
import cv2
from PIL import Image
import streamlit as st

MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
DP = (st.sidebar.slider("DP", 0, 200, 5))*(0.01)
Param1 = st.sidebar.slider("Parameter 1", 1, 200, 1)
Param2 = st.sidebar.slider("Parameter 2", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
#img = cv2.imread("/Users/josephtemplet/Desktop/work/housing2.jpg")
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "image path")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
while True:
    img = cv2.imread(args["image"])
    if img is None:
        break
    cv2.imshow("preview",img)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#detect circles in the image
#circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, param1=40,minRadius=10,maxRadius=35)
    circles = cv2.HoughCircles(gray, 
        cv2.HOUGH_GRADIENT, minDist=MinDist,
                           dp=DP,
                           param1=Param1,
                           param2=Param2,
                           minRadius=MinRadius,
                           maxRadius=MaxRadius)
    #print(len(circles[0][0]))



# ensure at least some circles were found
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    # count = count+1   

    # print(count) 

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
        #cv2.imshow("output", np.hstack([output]))
        #cv2.imwrite('output.jpg',np.hstack([output]),[cv2.IMWRITE_JPEG_QUALITY, 70])
        st.image("output", np.hstack([output]))
        cv2.waitKey(0)
        k = cv2.waitKey(0) & 0xFF
    
        if k == ord('c'): #you can put any key here
            break
#cap.release()
cv2.destroyAllWindows()
#/Users/josephtemplet/Desktop/work/

#python pipe-counting-code-for-housing.py --image /Users/josephtemplet/Desktop/work/housing2.jpg


#command line prompt: python Desktop/work/pipe-counting-code-for-housing.py --image /Users/josephtemplet/Desktop/work/housing2.jpg ###

#python - 

