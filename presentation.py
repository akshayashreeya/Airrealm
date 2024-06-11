import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# Variables for dynamic threshold and cooldown
cooldown_time = 1.5  # in seconds
last_swipe_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]

            # Detect swipe right gesture
            if x > frame.shape[1] * 0.9:  # Swipe right if finger tip is on the rightmost 10% of the frame
                if time.time() - last_swipe_time > cooldown_time:
                    pyautogui.press('right')  # Simulate right arrow key press
                    print("Swipe Right Detected")
                    last_swipe_time = time.time()
                    break

            # Detect swipe left gesture
            elif x < frame.shape[1] * 0.1:  # Swipe left if finger tip is on the leftmost 10% of the frame
                if time.time() - last_swipe_time > cooldown_time:
                    pyautogui.press('left')  # Simulate left arrow key press
                    print("Swipe Left Detected")
                    last_swipe_time = time.time()
                    break

    cv2.imshow('Presentation Controller', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
