import streamlit as st
import cv2
import threading
import numpy as np
import time

object_detector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=80)
MinDist = st.sidebar.slider("minimum distance", 1, 200, 1)
dp = (st.sidebar.slider("DP", 0, 200, 5)) * 0.01
max_canny_threshold = st.sidebar.slider("Parameter 1", 1, 200, 1)
marker_threshold = st.sidebar.slider("Parameter 2", 1, 200, 1)
MinRadius = st.sidebar.slider("minradius", 0, 200, 1)
MaxRadius = st.sidebar.slider("maxradius", 0, 200, 1)
detect_edges = st.sidebar.checkbox("show edge detection")
show_circles = st.sidebar.checkbox("show radius limits")

# Global variable to store the latest captured frame
captured_frame = None
lock = threading.Lock()


def capture_frames():
    global captured_frame
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from the webcam")
            break

        mask = object_detector.apply(frame)
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

        with lock:
            captured_frame = frame

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()


def display_frames():
    global captured_frame
    while True:
        with lock:
            frame = captured_frame

        if frame is not None:
            st.image(frame, channels="BGR")
        else:
            st.write("Waiting for frames...")

        # Delay to control the frame rate of the display
        time.sleep(0.01)


if __name__ == '__main__':
    # Create separate threads for image capture and display
    capture_thread = threading.Thread(target=capture_frames)
    display_thread = threading.Thread(target=display_frames)

    # Start the threads
    capture_thread.start()
    display_thread.start()

    # Wait for the threads to finish
    capture_thread.join()
    display_thread.join()