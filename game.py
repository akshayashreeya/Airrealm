import cv2
import mediapipe as mp
import time
from key import PressKey, ReleaseKey

up_key_pressed = 0x48
down_key_pressed = 0x50
right_key_pressed = 0x4D
left_key_pressed = 0x4B
space_key_pressed = 0x39  # Space key code

tipIds = [4, 8, 12, 16, 20]

time.sleep(2.0)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        keyPressed = False
        break_pressed = False
        accelerator_pressed = False
        key_count = 0
        key_pressed = 0

        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

        fingers = []

        if len(lmList) != 0:
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Detecting if all five fingers are raised
            if sum(fingers) == 5:
                fingers.append(1)
            else:
                fingers.append(0)

            total = fingers.count(1)

            cv2.rectangle(image, (0, 480), (300, 425), (50, 50, 255), -2)
            cv2.rectangle(image, (640, 480), (400, 425), (50, 50, 255), -2)

            cv2.putText(image, str(total), (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            print(total)

            if total == 1:
                cv2.putText(image, "UP", (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                PressKey(up_key_pressed)
                key_pressed = up_key_pressed
                accelerator_pressed = True
                keyPressed = True
                current_key_pressed.add(up_key_pressed)
                key_count += 1
            elif total == 2:
                cv2.putText(image, "LEFT", (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                PressKey(left_key_pressed)
                key_pressed = left_key_pressed
                accelerator_pressed = True
                keyPressed = True
                current_key_pressed.add(left_key_pressed)
                key_count += 1
            elif total == 3:
                cv2.putText(image, "RIGHT", (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                PressKey(right_key_pressed)
                key_pressed = right_key_pressed
                accelerator_pressed = True
                keyPressed = True
                current_key_pressed.add(right_key_pressed)
                key_count += 1
            elif total == 4:
                cv2.putText(image, "DOWN", (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                PressKey(down_key_pressed)
                key_pressed = down_key_pressed
                accelerator_pressed = True
                keyPressed = True
                current_key_pressed.add(down_key_pressed)
                key_count += 1
            elif total == 5:
                cv2.putText(image, "BOOST", (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                PressKey(space_key_pressed)
                key_pressed = space_key_pressed
                accelerator_pressed = True
                keyPressed = True
                current_key_pressed.add(space_key_pressed)
                key_count += 1

        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count == 1 and len(current_key_pressed) == 2:
            for key in current_key_pressed:
                if key_pressed != key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()

        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
