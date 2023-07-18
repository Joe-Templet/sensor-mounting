import cv2
import numpy as np
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2
#cap = cv2.VideoCapture(0)
img = cv2.imread("/Users/josephtemplet/Desktop/work/housing2.jpg")

#object_detector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
while True:
    
    #ret, frame = cap.read()
    #if not ret: break
    # Read image.

    #mask = object_detector.apply(frame)
    #img = cv2.imread('frame', cv2.IMREAD_COLOR)
    # Convert to grayscale.
    grayframe = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurframe = cv2.GaussianBlur(grayframe, (17,17), 0)
    # Blur using 3 * 3 kernel.
    #gray_blurred = cv2.blur(gray, (3, 3))
    
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(blurframe, 
                cv2.HOUGH_GRADIENT, 0.9, 1, param1 = 20,
                param2 = 20, minRadius = 1, maxRadius = 100)
    
    # Draw circles that are detected.
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        chosen = None
        for i in detected_circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0],prevCircle[1]) <= dist (i[0],i[1,prevCircle[0], prevCircle[1]]): 
                    chosen = i
        cv2.circle(img, (chosen[0],chosen[1]), 1, (0,100,100), 3)
        cv2.circle(img, (chosen[0],chosen[1]),chosen[2], (255,0,255), 3)
        prevCircle = chosen
        #for pt in detected_circles[0, :]:
            #a, b, r = pt[0], pt[1], pt[2]
    
            # Draw the circumference of the circle.
            #cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
    
            # Draw a small circle (of radius 1) to show the center.
            #cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

    cv2.imshow("Detected Circle", img)
    
    
    
    k = cv2.waitKey(0) & 0xFF
    
    if k == ord('c'): # you can put any key here
        break
#cap.release()
cv2.destroyAllWindows()

