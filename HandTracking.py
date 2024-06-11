import cv2
import mediapipe as mp
import time
from PIL import Image, ImageTk
from tkinter import Tk, Label, Canvas, Button
from enum import Enum
import threading

class HandGesture(Enum):
    NONE = 0
    THUMBS_UP = 1

class HandDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.pTime = 0
        self.thumb_up_counter = 0
        self.current_gesture = HandGesture.NONE
        self.running = True

    def find_hands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                thumb_up_detected = False
                wrist = handLms.landmark[0]
                thumb_tip = handLms.landmark[4]

                # Calculate vector from wrist to thumb tip
                thumb_vector = (thumb_tip.x - wrist.x, thumb_tip.y - wrist.y, thumb_tip.z - wrist.z)

                # Normalize the vector
                thumb_length = (thumb_vector[0]**2 + thumb_vector[1]**2 + thumb_vector[2]**2)**0.5
                thumb_vector = (thumb_vector[0] / thumb_length, thumb_vector[1] / thumb_length, thumb_vector[2] / thumb_length)

                # Check if the thumb is pointing upwards relative to the wrist
                if thumb_vector[1] < -0.8:
                    thumb_up_detected = True

                if thumb_up_detected:
                    self.thumb_up_counter += 1
                else:
                    self.thumb_up_counter = 0

                if self.thumb_up_counter >= 20:  # Adjust the threshold for thumb-up detection
                    self.thumb_up_counter = 0
                    self.current_gesture = HandGesture.THUMBS_UP
                else:
                    self.current_gesture = HandGesture.NONE

                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        else:
            self.current_gesture = HandGesture.NONE

    def display_fps(self, img):
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    def terminate(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
        root.destroy()

def update_camera_feed():
    while hand_detector.running:
        success, img = hand_detector.cap.read()
        if success:
            hand_detector.find_hands(img)
            if hand_detector.current_gesture == HandGesture.THUMBS_UP:
                hand_detector.terminate()
                return
            hand_detector.display_fps(img)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (800, 600))  # Adjust the size
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)

            camera_frame.create_image(0, 0, anchor="nw", image=img)
            camera_frame.img = img

            root.update()  # Update the GUI to display the new camera frame

if __name__ == "__main__":
    root = Tk()
    root.title("Hand Tracking")

    hand_detector = HandDetector()

    label = Label(root, text="Hand Tracking", font=("Helvetica", 16))
    label.pack()

    camera_frame = Canvas(root, width=800, height=600)
    camera_frame.pack()

    end_button = Button(root, text="End", command=hand_detector.terminate)
    end_button.pack(side="bottom")

    # Start a thread to update the camera feed
    camera_thread = threading.Thread(target=update_camera_feed)
    camera_thread.start()

    root.mainloop()
