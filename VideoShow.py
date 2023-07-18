from threading import Thread
import cv2
import streamlit as st
from queue import Queue

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """
    st.set_page_config(layout="wide")   
    
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        self.q = Queue()
        Thread(target=self.show, args=(self.q)).start()
        return self

    def show(self):
        while not self.stopped:
            #cv2.imshow("Video", self.frame)
            st.image(self.frame,channels="BGR", width=640)  #channels="BGR", use_column_width=True
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True