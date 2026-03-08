# 🖐️ Hand Gesture Detector

Real-time hand gesture recognition using OpenCV and MediaPipe. Detects both hands simultaneously, works correctly whether your palm is facing toward or away from the camera.

---

## ✨ Features

- 🖐️ Detects up to **2 hands** simultaneously
- 🔄 Works for both **palm-facing** and **back-of-hand** orientations
- 🤚 Supports **Left & Right hand** detection separately
- 📐 **Rotation-corrected** finger tracking (works at any hand angle)
- ⚡ Real-time processing via webcam

---

## 🤟 Supported Gestures

| Gesture | Description |
|---|---|
| ✊ **Punch** | All fingers closed |
| 🖐️ **Open Hand** | All fingers open |
| ✌️ **Peace** | Index + Middle finger open |
| 👍 **Like** | Only thumb open |
| 🖕 **Middle Finger** | Only middle finger open |

---

## 🛠️ Requirements

- Python 3.7+
- OpenCV
- MediaPipe

Install dependencies:

```bash
pip install opencv-python mediapipe
```

---

## 🚀 Usage

```bash
python hand_detector.py
```

- Press **`q`** to quit

> **Note:** The script uses `cv2.VideoCapture(1)` by default. If your webcam is not detected, change `1` to `0`:
> ```python
> cap = cv2.VideoCapture(0)
> ```

---

## 📁 Project Structure

```
hand-gesture-detector/
│
├── hand_detector.py   # Main script
└── README.md
```

---

## 🧠 How It Works

1. **MediaPipe Hands** detects 21 hand landmarks per hand
2. Hand angle is calculated using the wrist and middle finger base to normalize rotation
3. All landmarks are rotated to a standard upright position
4. **Palm direction** is determined by comparing the x positions of the pinky base (landmark 17) and index base (landmark 5) — no depth/z dependency
5. Finger states (open/closed) are computed based on tip vs base y-positions in the corrected coordinate space
6. Gesture is matched against predefined finger patterns

---

## 📸 Demo

```
Right: [1, 1, 1, 1, 1] → Open Hand
Left:  [0, 0, 0, 0, 0] → Punch
Right: [0, 1, 1, 0, 0] → Peace
```

---

## 📄 License

MIT License — free to use and modify.
