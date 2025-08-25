# ✋ Hand Tracking Game (OpenCV + cvzone)  

This project implements **real-time hand tracking** and a fun **hand-controlled game** using **OpenCV**, **cvzone**, and a webcam.  
It leverages computer vision to detect your hand, measure its distance, and interact with on-screen objects without a controller!  

---

## 🎮 Features  
- **Hand Distance Tracking**:  
  - `DisTrcking.py` estimates the distance of your hand from the webcam in **centimeters** using calibration.  

- **Interactive Hand Game**:  
  - `Game.py` spawns targets (circles) at random positions.  
  - Use your **hand** to “touch” the circle and score points.  
  - Game runs for **40 seconds** with live score and timer.  

---

1. Clone this repository  
   ```bash
   git clone https://github.com/<your-username>/handTracking.git
   cd handTracking

2. Install dependencies
   ``` pip install opencv-python cvzone numpy

3. Run hand distance tracking
   ``` python DisTrcking.py

4. Run the game
   ``` python Game.py


