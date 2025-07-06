# Drowsiness and Yawn Detection Using Raspberry Pi 02W

This project detects driver drowsiness and yawning in real-time using a Raspberry Pi 02W, a camera module, and a buzzer. The system leverages facial landmark detection to monitor the driver's eyes and mouth, and triggers a buzzer alarm if signs of drowsiness or yawning are detected.

## Features

- **Drowsiness Detection:** Alerts when the driver's eyes remain closed for a threshold duration.
- **Yawn Detection:** Alerts when the driver's mouth remains open (yawning) for a threshold duration.
- **Real-time Monitoring:** Processes video stream from the Pi camera.
- **Physical Alert:** Activates a buzzer for immediate warning.

## Hardware Requirements

- Raspberry Pi 02W (or any compatible Pi)
- Pi Camera Module (or supported USB camera)
- Buzzer
- Jumper wires

## Software Requirements

- Python 3
- [OpenCV](https://opencv.org/) (`cv2`)
- [dlib](http://dlib.net/)
- [imutils](https://github.com/jrosebr1/imutils)
- [scipy](https://scipy.org/)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) (for GPIO control)
- Pre-trained dlib facial landmark predictor: `shape_predictor_68_face_landmarks.dat`

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/VEDANKAR/Drowsiness-and-Yawan-Detection-using-Raspberry-Pi-02W.git
   cd Drowsiness-and-Yawan-Detection-using-Raspberry-Pi-02W
   ```

2. **Install dependencies**

   ```bash
   pip install opencv-python dlib imutils scipy RPi.GPIO
   ```

   > **Note:** On Raspberry Pi, you may need to install OpenCV and dlib from source for full compatibility.

3. **Download the pre-trained facial landmark model**

   - Download `shape_predictor_68_face_landmarks.dat` from [dlib model zoo](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
   - Extract it and place it in the same directory as `code.py`.

4. **Hardware Setup**

   - Connect the buzzer to GPIO pin 18 and GND on the Raspberry Pi.

## Usage

1. **Connect the camera and buzzer to the Raspberry Pi.**
2. **Run the detection script:**

   ```bash
   python3 code.py
   ```

3. The application will start capturing video. If drowsiness or yawning is detected, a warning message will be displayed on the frame and the buzzer will sound.

4. Press <kbd>ESC</kbd> to exit the application.

## Configuration

- Adjust the following thresholds in `code.py` if needed:
  - `EAR_THRESH`: Eye Aspect Ratio threshold for drowsiness (default: `0.25`)
  - `EAR_CONSEC_FRAMES`: Number of consecutive frames for drowsiness alert (default: `20`)
  - `MAR_THRESH`: Mouth Aspect Ratio threshold for yawn detection (default: `0.7`)

## File Structure

```
.
├── code.py
├── README.md
└── shape_predictor_68_face_landmarks.dat
```

## References

- [dlib: Facial landmark detector](http://dlib.net/)
- [Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR) papers](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
- [imutils documentation](https://github.com/jrosebr1/imutils)

## Troubleshooting

- **Camera not detected:** Ensure your Pi camera is enabled (`raspi-config`) and properly connected.
- **dlib errors:** Make sure you installed dlib for your Python version and architecture.
- **Buzzer not working:** Double-check wiring and GPIO pin configuration.



---
**Developed by [VEDANKAR](https://github.com/VEDANKAR)**