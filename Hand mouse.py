import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Set up webcam and screen
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
clicking = False
last_click_time = 0
CLICK_DELAY = 0.4  # seconds between clicks to avoid multiple fast clicks

# Define control zone (central region of camera)
ZONE_TOP = 0.33
ZONE_BOTTOM = 0.67
ZONE_LEFT = 0.33
ZONE_RIGHT = 0.67

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    h, w, _ = frame.shape

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            idx_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            idx_x = int(idx_tip.x * w)
            idx_y = int(idx_tip.y * h)
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            # Clamp tip coordinates to control zone and remap to full screen
            norm_x = min(max(idx_tip.x, ZONE_LEFT), ZONE_RIGHT)
            norm_y = min(max(idx_tip.y, ZONE_TOP), ZONE_BOTTOM)
            remap_x = (norm_x - ZONE_LEFT) / (ZONE_RIGHT - ZONE_LEFT)
            remap_y = (norm_y - ZONE_TOP) / (ZONE_BOTTOM - ZONE_TOP)

            screen_x = int(remap_x * screen_width)
            screen_y = int(remap_y * screen_height)
            # Clamp to avoid PyAutoGUI fail-safe trigger
            screen_x = max(1, min(screen_x, screen_width - 2))
            screen_y = max(1, min(screen_y, screen_height - 2))
            pyautogui.moveTo(screen_x, screen_y)

            # Calculate distance between index finger tip and thumb tip
            distance = math.hypot(thumb_x - idx_x, thumb_y - idx_y)
            TOUCH_THRESHOLD = 30
            current_time = time.time()

            if distance < TOUCH_THRESHOLD:
                if not clicking and (current_time - last_click_time) > CLICK_DELAY:
                    clicking = True
                    last_click_time = current_time
                    pyautogui.click()
                    cv2.circle(frame, (idx_x, idx_y), 12, (0, 255, 0), cv2.FILLED)
            else:
                clicking = False

    cv2.imshow('Virtual Mouse - Short Control Zone with Precise Click', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
