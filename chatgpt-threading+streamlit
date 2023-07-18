import cv2
import streamlit as st
import numpy as np
import threading

def display_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame from the webcam")
            break

        # Convert BGR frame to RGB for displaying in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in Streamlit
        st.image(frame_rgb, channels="RGB", use_column_width=True)

        # Check if 'q' key is pressed to stop the program
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

def main():
    st.title("Webcam Video Stream")
    st.write("Press the 'Start' button to start streaming video from your webcam.")
    st.write("Press 'Stop' to stop the streaming.")

    # Create a stop event to signal the thread to stop
    stop_event = threading.Event()

    if st.button("Start"):
        # Create a separate thread for displaying the webcam feed
        thread = threading.Thread(target=display_webcam)

        # Start the thread
        thread.start()

        # Wait for the 'Stop' button to be pressed
        st.button("Stop")

        # Set the stop event to stop the thread
        stop_event.set()

        # Wait for the thread to finish
        thread.join()

if __name__ == "__main__":
    main()
    