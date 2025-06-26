import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyautogui
import time

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Hand Detector
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Get screen size
screen_w, screen_h = pyautogui.size()

# Variables for slicing effect
prev_x, prev_y = 0, 0
slicing = False
speed_threshold = 30  # Speed threshold for slicing
marker_x, marker_y = 0, 0  # To track marker position

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Error: Camera not detected!")
        break

    img = cv2.flip(img, 1)  # Mirror effect
    hands, img = detector.findHands(img)  # Detect hands

    if hands:
        lmList = hands[0]['lmList']  # Get landmark positions
        ind_x, ind_y = lmList[8][0], lmList[8][1]  # Index finger tip

        # Convert to screen coordinates
        screen_x = int(np.interp(ind_x, (100, 540), (0, screen_w)))
        screen_y = int(np.interp(ind_y, (100, 380), (0, screen_h)))

        # Move cursor to finger position
        pyautogui.moveTo(screen_x, screen_y, duration=0.01)

        # Calculate movement speed
        movement_speed = np.sqrt((screen_x - prev_x) ** 2 + (screen_y - prev_y) ** 2)

        # Activate slicing only when moving fast
        if movement_speed > speed_threshold:
            if not slicing:
                pyautogui.mouseDown()
                slicing = True
        else:
            if slicing:
                pyautogui.mouseUp()
                slicing = False

        prev_x, prev_y = screen_x, screen_y  # Update position

        # Update marker position
        marker_x, marker_y = screen_x, screen_y

    # Overlay a marker on screen
    overlay = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
    cv2.circle(overlay, (marker_x, marker_y), 10, (0, 255, 0), -1)  # Green marker

    # Show the overlay
    cv2.imshow("Game Cursor", overlay)
    cv2.imshow("Webcam Feed", img)

    # Press 'Esc' to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
