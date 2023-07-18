import streamlit as st
import cv2
import multiprocessing as mp
import numpy as np

object_detector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
dp = (st.sidebar.slider("DP", 0, 200, 5)) * 0.01
max_canny_threshold = st.sidebar.slider("Parameter 1", 1, 200, 1)
marker_threshold = st.sidebar.slider("Parameter 2", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
detect_edges = st.sidebar.checkbox("show edge detection")
show_circles = st.sidebar.checkbox("show radius limits")

def capture_frames(output):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from the webcam")
            break
        output.put(frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

def display_frames(input):
    while True:
        frame = input.get()
        if frame is not None:
            #mask = object_detector.apply(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 5)
            circles = cv2.HoughCircles(
                blur,
                cv2.HOUGH_GRADIENT,
                minDist=MinDist,
                dp=dp,
                param1=max_canny_threshold,
                param2=marker_threshold,
                minRadius=MinRadius,
                maxRadius=MaxRadius,
            )

            if circles is not None:
                detected_circles = np.uint16(np.around(circles))
                for (x, y, r) in detected_circles[0, :]:
                    cv2.circle(frame, (x, y), r, (0, 0, 0), 3)
                    cv2.circle(frame, (x, y), 2, (0, 255, 255), 3)

            if detect_edges:
                frame = cv2.Canny(frame, max_canny_threshold / 2, max_canny_threshold)

            if show_circles:
                cv2.circle(frame, (100, 100), MinRadius, (0, 100, 100), 3)
                cv2.circle(frame, (100, 100), MaxRadius, (0, 100, 100), 3)

            st.image(frame, channels="BGR")

        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    # Create a separate process for capturing frames
    output = mp.Queue()
    capture_process = mp.Process(target=capture_frames, args=(output,))
    capture_process.start()

    # Display the frames in the Streamlit app
    display_frames(output)

    # Terminate the process
    capture_process.terminate()
    