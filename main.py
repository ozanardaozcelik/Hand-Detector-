import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

TIPS = [4, 8, 12, 16, 20]

def get_hand_angle(landmarks):
    wrist = landmarks[0]
    middle_base = landmarks[9]
    dx = middle_base.x - wrist.x
    dy = middle_base.y - wrist.y
    return math.degrees(math.atan2(dy, dx))

def rotate_point(x, y, angle_deg):
    angle_rad = math.radians(angle_deg)
    new_x = x * math.cos(angle_rad) + y * math.sin(angle_rad)
    new_y = -x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return new_x, new_y

def get_finger_status(landmarks, hand_label):
    angle = get_hand_angle(landmarks)
    correction = -angle + 90

    def r(lm):
        return rotate_point(lm.x, lm.y, correction)

    if hand_label == "Right":
        palm_facing = landmarks[17].x > landmarks[5].x
    else:
        palm_facing = landmarks[17].x < landmarks[5].x

    fingers = []

    tx4, _ = r(landmarks[4])
    tx3, _ = r(landmarks[3])

    if palm_facing:
        if hand_label == "Right":
            fingers.append(1 if tx4 > tx3 else 0)
        else:
            fingers.append(1 if tx4 < tx3 else 0)
    else:
        if hand_label == "Right":
            fingers.append(1 if tx4 < tx3 else 0)
        else:
            fingers.append(1 if tx4 > tx3 else 0)

    for tip_id in TIPS[1:]:
        _, tip_y = r(landmarks[tip_id])
        _, base_y = r(landmarks[tip_id - 2])
        fingers.append(1 if tip_y > base_y else 0)

    return fingers

def detect_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "Punch"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Open Hand"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Like"
    elif fingers == [0, 0, 1, 0, 0]:
        return "Middle Finger"
    else:
        return "?"

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_lms, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

            hand_label = handedness.classification[0].label
            lm_list = hand_lms.landmark

            fingers = get_finger_status(lm_list, hand_label)
            gesture = detect_gesture(fingers)

            print(f"{hand_label}: {fingers}")

            x_coords = [lm.x for lm in lm_list]
            y_coords = [lm.y for lm in lm_list]
            h, w, _ = frame.shape
            x_min = int(min(x_coords) * w)
            y_min = int(min(y_coords) * h) - 30

            cv2.putText(frame, f"{hand_label}: {gesture}",
                        (max(x_min, 10), max(y_min, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
