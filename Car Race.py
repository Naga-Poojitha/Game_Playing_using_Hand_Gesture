import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.5, maxHands=2)
cap = cv2.VideoCapture(0)
cap.set(3, 600)  # Width
cap.set(4, 480)  # Height

while True:
    success, img = cap.read()
    img = cv2.flip(img, flipCode=1)  # Flip horizontally
    hands, img = detector.findHands(img)  # Detect hands

    if hands:  # Ensure hands are detected
        hand = hands[0]  # Consider first detected hand
        if hand["type"] == "Left":
            fingers = detector.fingersUp(hand)
            totalFingers = fingers.count(1)
            # Hand Detector
            detector = HandDetector(detectionCon=0.8, maxHands=1)

            cv2.putText(img, f'Fingers: {totalFingers}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            if totalFingers == 5:
                pyautogui.keyDown("right")
                pyautogui.keyUp("left")

            elif totalFingers == 0:
                pyautogui.keyDown("left")
                pyautogui.keyUp("right")

    cv2.imshow("Camera_Feed", img)
    cv2.waitKey(1)