import cv2
import pyautogui
import tkinter as tk
from threading import Thread
import numpy as np

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")

        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.recording = False
        self.video_writer = None

    def start_recording(self):
        self.recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        screen_size = (1920, 1080)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.video_writer = cv2.VideoWriter("screen_record.avi", fourcc, 20.0, screen_size)

        def record_screen():
            try:
                while self.recording:
                    img = pyautogui.screenshot()
                    frame = np.array(img)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.video_writer.write(frame)
            except KeyboardInterrupt:
                pass
            finally:
                self.video_writer.release()

        # Start recording in a separate thread
        self.record_thread = Thread(target=record_screen)
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_thread.join()  # Wait for the recording thread to finish
        self.video_writer.release()

        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    recorder = ScreenRecorder(root)
    root.mainloop()
