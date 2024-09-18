import sys
import threading
import pyautogui
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from datetime import datetime

class ScreenRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Recorder")
        self.setGeometry(100, 100, 400, 200)  # Adjusted window size for better spacing

        # Default save location (initially current directory)
        self.save_location = ""

        # Layout for the buttons and label
        layout = QVBoxLayout()

        # Welcome text (QLabel) - centered
        self.welcome_label = QLabel("Welcome to Ankita's Screen Recorder", self)
        self.welcome_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.welcome_label.setAlignment(Qt.AlignCenter)  # Center the text horizontally
        layout.addWidget(self.welcome_label)

        # Button to choose the save location
        self.choose_location_button = QPushButton("Choose Save Location", self)
        self.choose_location_button.clicked.connect(self.choose_save_location)
        layout.addWidget(self.choose_location_button)

        # Start button
        self.start_button = QPushButton("Start Recording", self)
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)

        # Stop button (Initially disabled)
        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)

        # Set the layout for the window
        self.setLayout(layout)

        # Recording status flag
        self.is_recording = False

    # Method to choose the save location
    def choose_save_location(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Choose Save Location", "", "MP4 Files (*.mp4)")
        if file_name:  # If the user has chosen a file
            self.save_location = file_name
            print(f"Save location set to: {self.save_location}")

    # Method to generate a unique filename if the user has not specified one
    def generate_unique_filename(self):
        if not self.save_location:  # If no custom save location, generate a default file
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"AP_{current_time}.mp4"  # Default file name with time stamp
            return filename
        else:
            return self.save_location  # Use the custom save location provided by the user

    # Method to start the recording
    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.start_button.setEnabled(False)  # Disable the start button during recording
            self.stop_button.setEnabled(True)  # Enable the stop button during recording
            self.recording_thread = threading.Thread(target=self.record_screen)
            self.recording_thread.start()
            print("Recording started...")

    # Method to stop the recording
    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.setEnabled(True)  # Enable the start button when recording stops
            self.stop_button.setEnabled(False)  # Disable the stop button when recording stops
            print("Recording stopped.")

    # Method to record the screen
    def record_screen(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        output_filename = self.generate_unique_filename()  # Get the user-defined or default filename
        out = cv2.VideoWriter(output_filename, fourcc, 20.0, screen_size)

        while self.is_recording:
            # Capture the screen
            img = pyautogui.screenshot()

            # Convert the screenshot to a numpy array
            frame = np.array(img)

            # Convert the color from RGB to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Write the frame to the output video
            out.write(frame)

        # Release the video writer after recording
        out.release()

# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenRecorderApp()
    window.show()
    sys.exit(app.exec_())