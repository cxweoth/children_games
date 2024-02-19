"""
Not complete yet
他會直接放大整個應用程式，而不是放大應用程式裡的內容，這個先放一下，目前不急著做這個
"""

import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_distance = None
zoom_threshold = 0.05  

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

            if prev_distance is not None:
                distance_change = distance - prev_distance
                if distance_change > zoom_threshold:
                    pyautogui.hotkey('command', '+')  # 放大
                elif distance_change < -zoom_threshold:
                    pyautogui.hotkey('command', '-')  # 缩小

            prev_distance = distance

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
