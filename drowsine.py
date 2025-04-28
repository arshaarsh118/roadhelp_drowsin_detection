import cv2
import dlib
import time
import os
import numpy as np
import threading
from scipy.spatial import distance as dist
from imutils import face_utils
from playsound import playsound

# Constants
EYE_AR_THRESH = 0.25  # Eye Aspect Ratio (EAR) threshold
EYE_AR_CONSEC_FRAMES = 20  # Number of consecutive frames for drowsiness detection

COUNTER = 0  # Frame counter for closed eyes
ALARM_ON = False  # Alarm status

# Load pre-trained face detector and landmark predictor
detector = dlib.get_frontal_face_detector()

PREDICTOR_PATH = r"C:\Users\arsha\OneDrive\Desktop\college_project\ST_Marys_BVOC\RoadHelp_Web\shape_predictor_68_face_landmarks.dat"
if not os.path.exists(PREDICTOR_PATH):
    print(f"Error: The file {PREDICTOR_PATH} was not found. Ensure the path is correct.")
    exit()

predictor = dlib.shape_predictor(PREDICTOR_PATH)

# Indices for left and right eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Function to calculate Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Function to play alarm in a separate thread
def play_alarm():
    global ALARM_ON
    if not ALARM_ON:
        ALARM_ON = True
        playsound("alarm.mp3")
        ALARM_ON = False

# Start video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to capture frame. Exiting...")
        break

    # Ensure frame is in the correct format (BGR) before conversion
    if frame.dtype != np.uint8:
        print("Frame is not 8-bit. Converting...")
        frame = frame.astype(np.uint8)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Debugging: Check grayscale image properties
    print(f"Grayscale shape: {gray.shape}, dtype: {gray.dtype}")

    # Ensure grayscale is 8-bit
    if gray.dtype != np.uint8:
        print("Grayscale is not 8-bit. Converting...")
        gray = gray.astype(np.uint8)

    # Detect faces
    try:
        faces = detector(gray, 0)
    except RuntimeError as e:
        print(f"Error in face detection: {e}")
        continue

    if len(faces) == 0:
        print("No face detected.")

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Extract left and right eye landmarks
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # Compute EAR for both eyes
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Draw eye landmarks
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

        # Check if eyes are closed
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    threading.Thread(target=play_alarm, daemon=True).start()
                cv2.putText(frame, "DROWSINESS ALERT!", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            COUNTER = 0

    # Display output
    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()