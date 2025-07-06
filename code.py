import cv2
import dlib
import time
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import RPi.GPIO as GPIO

# GPIO setup for buzzer
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# EAR and MAR thresholds
EAR_THRESH = 0.25
EAR_CONSEC_FRAMES = 20
MAR_THRESH = 0.7

# Frame counters
COUNTER = 0
YAWN_COUNTER = 0

# Functions to calculate EAR and MAR
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[13], mouth[19])
    B = dist.euclidean(mouth[14], mouth[18])
    C = dist.euclidean(mouth[15], mouth[17])
    D = dist.euclidean(mouth[12], mouth[16])
    mar = (A + B + C) / (3.0 * D)
    return mar

# Load face detector and predictor
print("[INFO] Loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Ensure this is in same folder

# Grab landmark indexes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# Start video stream from Pi camera
print("[INFO] Starting video stream...")
cap = cv2.VideoCapture(0)
time.sleep(1.0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            mouth = shape[mStart:mEnd]

            ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0
            mar = mouth_aspect_ratio(mouth)

            # Draw contours
            cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (0, 0, 255), 1)

            # Drowsiness detection
            if ear < EAR_THRESH:
                COUNTER += 1
                if COUNTER >= EAR_CONSEC_FRAMES:
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    GPIO.output(BUZZER_PIN, GPIO.HIGH)
            else:
                COUNTER = 0
                GPIO.output(BUZZER_PIN, GPIO.LOW)

            # Yawn detection
            if mar > MAR_THRESH:
                YAWN_COUNTER += 1
                cv2.putText(frame, "YAWNING!", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
            else:
                YAWN_COUNTER = 0
                GPIO.output(BUZZER_PIN, GPIO.LOW)

            # Show EAR and MAR values
            cv2.putText(frame, f"EAR: {ear:.2f}", (480, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"MAR: {mar:.2f}", (480, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Drowsiness & Yawn Detection", frame)
        if cv2.waitKey(1) == 27:  # ESC to quit
            break

except KeyboardInterrupt:
    print("[INFO] Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
