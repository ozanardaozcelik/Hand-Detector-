# ✋ Hand Gesture Detector

A real-time hand gesture recognition project built with Python, OpenCV and MediaPipe.

---

## 🎯 Supported Gestures

| Gesture | Name |
|---|---|
| ✊ | Punch |
| ✋ | Open Hand |
| ✌️ | Peace |
| 👍 | Like |
| 🖕 | Middle Finger |

---

## 🛠️ Requirements

- Python 3.8+
- OpenCV
- MediaPipe 0.10.9
- Protobuf 3.20.3

---

## 📦 Installation

```bash
pip install protobuf==3.20.3
pip install mediapipe==0.10.9
pip install opencv-python
```

---

## 🚀 Usage

```bash
python main.py
```

- Press **Q** to quit
- Uses external camera by default (`VideoCapture(1)`) — change to `0` for built-in webcam

---

## 🧠 How It Works

MediaPipe detects **21 landmarks** on the hand. Each finger has a tip and base knuckle point. By comparing their coordinates:

- **y-axis** → finger up or down (index, middle, ring, pinky)
- **x-axis** → thumb open or closed

```
4   8  12  16  20   ← fingertips
|   |   |   |   |
3   7  11  15  19
|   |   |   |   |
2   6  10  14  18
|   |   |   |   |
1   5   9  13  17
 \  |   |   |  /
         0          ← wrist
```

The `get_finger_status()` function returns a list like `[thumb, index, middle, ring, pinky]` where `1 = open` and `0 = closed`. The `detect_gesture()` function matches this list to a known gesture.

---

## 📁 Project Structure

```
Hand Detector/
│
└── main.py
```

---

## 🙏 Credits

- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
