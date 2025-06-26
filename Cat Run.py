import cv2
import mediapipe as mp
import pyautogui
# import pygetwindow as gw


# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            # Get finger status
            index_finger_up = landmarks[8].y < landmarks[6].y
            middle_finger_up = landmarks[12].y < landmarks[10].y
            ring_finger_up = landmarks[16].y < landmarks[14].y
            pinky_finger_up = landmarks[20].y < landmarks[18].y

            # Count open fingers
            open_fingers = sum([index_finger_up, middle_finger_up, ring_finger_up, pinky_finger_up])

            # # Gesture Recognition
            if open_fingers == 1 and index_finger_up:  # One finger up → Move up
                pyautogui.press("up")

            elif open_fingers == 0:  # Fist closed → Move down
                pyautogui.press("down")

            elif open_fingers == 4:  # Four fingers open → Move right
                pyautogui.press("right")

            elif open_fingers == 2 and index_finger_up and middle_finger_up:  # Two fingers open → Move left
                pyautogui.press("left")

            # # Focus BlueStacks before sending keys
            # win = gw.getWindowsWithTitle('BlueStacks')
            # if win:
            #     win[0].activate()
            #
            # # Gesture Recognition and Control
            # if open_fingers == 1 and index_finger_up:  # One finger up → Move up
            #     pyautogui.press("up")
            #
            # elif open_fingers == 0:  # Fist closed → Move down
            #     pyautogui.press("down")
            #
            # elif open_fingers == 4:  # Four fingers open → Move right
            #     pyautogui.press("right")
            #
            # elif open_fingers == 2 and index_finger_up and middle_finger_up:  # Two fingers open → Move left
            #     pyautogui.press("left")


            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display webcam feed
    cv2.imshow("Hand Gesture Control", frame)

    # Exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
