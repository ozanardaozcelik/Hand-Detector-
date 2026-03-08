import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

TIPS = [4, 8, 12, 16, 20]

def get_finger_status(landmarks):
    fingers = []

    if landmarks[4].x > landmarks[3].x:  # < yerine > yaptık
        fingers.append(1)
    else:
        fingers.append(0)

    for tip_id in TIPS[1:]:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def detect_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "Punch ✊"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Open Hand ✋"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace ✌️"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Like 👍"
    elif fingers == [0, 0, 1, 0, 0]:
        return "Middle Finger 🖕"
    else:
        return "?"

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_lms in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

            lm_list = hand_lms.landmark
            fingers = get_finger_status(lm_list)
            gesture = detect_gesture(fingers)

            cv2.putText(frame, gesture, (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Hand Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
