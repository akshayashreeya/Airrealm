import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
from enum import Enum

class Gesture(Enum):
    SWIPE_RIGHT = 0
    SWIPE_LEFT = 1
    SWIPE_UP = 2
    SWIPE_DOWN = 3

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Variables for dynamic threshold and cooldown
cooldown_time = 1.5  # in seconds
last_swipe_time = time.time()
swipe_up_detected = False
swipe_down_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]
            y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0]

            # Calculate hand movement velocity
            if 'prev_x' in globals():
                velocity = abs(x - prev_x)
            else:
                velocity = 0

            # Adjust swipe threshold dynamically based on velocity
            swipe_threshold = max(50, min(200, int(velocity * 2)))

            # Detect swipe right gesture
            if 'prev_x' in globals() and x - prev_x > swipe_threshold:
                # Perform action when swipe right is detected
                if time.time() - last_swipe_time > cooldown_time:
                    pyautogui.hotkey('ctrl', 'right')  # Simulate keyboard control + right press
                    print("Swipe Right Detected")
                    last_swipe_time = time.time()
                    break

            # Detect swipe left gesture
            elif 'prev_x' in globals() and prev_x - x > swipe_threshold:
                # Perform action when swipe left is detected
                if time.time() - last_swipe_time > cooldown_time:
                    pyautogui.hotkey('ctrl', 'left')  # Simulate keyboard control + left press
                    print("Swipe Left Detected")
                    last_swipe_time = time.time()
                    break

            # Detect swipe down gesture
            elif 'prev_y' in globals() and prev_y - y > swipe_threshold:
                # Perform action when swipe down is detected
                if not swipe_down_detected:
                    pyautogui.keyDown('ctrl')  # Press control key
                    pyautogui.press('down')  # Simulate keyboard down press
                    swipe_down_detected = True
                    print("Swipe Down Detected")
                    last_swipe_time = time.time()
                break

            # Detect swipe up gesture
            elif 'prev_y' in globals() and y - prev_y > swipe_threshold:
                # Perform action when swipe up is detected
                if not swipe_up_detected:
                    pyautogui.keyDown('ctrl')  # Press control key
                    pyautogui.press('up')  # Simulate keyboard up press
                    swipe_up_detected = True
                    print("Swipe Up Detected")
                    last_swipe_time = time.time()
                break

            else:
                if swipe_up_detected:
                    pyautogui.press('up')  # Simulate continuous keyboard up press
                    print("Volume Up")
                if swipe_down_detected:
                    pyautogui.press('down')  # Simulate continuous keyboard down press
                    print("Volume Down")

            # Update previous x and y positions
            prev_x, prev_y = x, y

    else:
        # If no hand is detected, release the control key
        if swipe_up_detected or swipe_down_detected:
            pyautogui.keyUp('ctrl')  # Release the control key
            swipe_up_detected = False
            swipe_down_detected = False

    cv2.imshow('Media Player Controller', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
