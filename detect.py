import cv2
import dlib
import numpy as np
import imutils
from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
import winsound
from time import sleep
from datetime import datetime

# Placeholder functions
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[2], mouth[10])
    B = dist.euclidean(mouth[4], mouth[8])
    C = dist.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

def getHeadTiltAndCoords(size, image_points, frame_height):
    return (0, (size[1]//2, 0), (size[1]//2, size[0]), (size[1]//2, size[0]//2))

def perform_yolo_detection(frame, lid):
    pass

class detection:
    def __init__(self, detected, time, date, status, driver_id):
        self.detected = detected
        self.time = time
        self.date = date
        self.status = status
        self.driver_id = driver_id
    def save(self):
        print(f"Saving detection: {self.detected}, Driver ID: {self.driver_id}")

def detect(lid):
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor_path = r"static/shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    print("[INFO] initializing camera...")
    vs = VideoStream(src=0).start()  # Try src=1 or -1 if 0 fails
    sleep(2.0)

    frame_width = 1024
    frame_height = 576

    image_points = np.array([
        (359, 391),  # Nose tip
        (399, 561),  # Chin
        (337, 297),  # Left eye left corner
        (513, 301),  # Right eye right corner
        (345, 465),  # Left mouth corner
        (453, 469)   # Right mouth corner
    ], dtype="double")

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = (49, 68)

    EYE_AR_THRESH = 0.25
    MOUTH_AR_THRESH = 0.79
    EYE_AR_CONSEC_FRAMES = 3
    COUNTER = 0

    while True:
        frame = vs.read()
        if frame is None:
            print("Failed to grab frame. Check webcam connection.")
            break

        # Resize and validate frame
        frame = imutils.resize(frame, width=frame_width, height=frame_height)
        if frame.size == 0 or frame.shape[0] == 0 or frame.shape[1] == 0:
            print("Invalid frame size. Skipping this frame.")
            continue

        # Ensure frame is 8-bit unsigned integer
        if frame.dtype != np.uint8:
            print(f"Converting frame from {frame.dtype} to uint8")
            frame = frame.astype(np.uint8)

        # Convert to grayscale and validate
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error as e:
            print(f"Grayscale conversion failed: {e}")
            continue

        if gray is None or gray.size == 0:
            print("Grayscale image is None or empty. Skipping this frame.")
            continue

        if gray.dtype != np.uint8:
            print(f"Converting gray from {gray.dtype} to uint8")
            gray = gray.astype(np.uint8)

        # Debug info
        print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")
        print(f"Gray shape: {gray.shape}, dtype: {gray.dtype}")

        size = gray.shape
        rects = detector(gray, 0)

        if len(rects) > 0:
            text = "{} face(s) found".format(len(rects))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        for rect in rects:
            flag = 0
            (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH), (0, 255, 0), 1)

            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # Eye detection
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    cv2.putText(frame, "Eyes Closed!", (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    winsound.Beep(2500, 500)
                    q = detection(detected='Eyes Closed', time=datetime.now().time(), date=datetime.now().date(), status=1, driver_id=lid)
                    q.save()
                else:
                    flag += 1
            else:
                COUNTER = 0
                flag += 1

            # Mouth detection
            mouth = shape[mStart:mEnd]
            mouthMAR = mouth_aspect_ratio(mouth)
            mouthHull = cv2.convexHull(mouth)
            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
            cv2.putText(frame, "MAR: {:.2f}".format(mouthMAR), (650, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if mouthMAR > MOUTH_AR_THRESH:
                cv2.putText(frame, "Yawning!", (800, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                winsound.Beep(2500, 500)
                q = detection(detected='Yawning', time=datetime.now().time(), date=datetime.now().date(), status=1, driver_id=lid)
                q.save()
            else:
                flag += 1

            # Head pose
            for (i, (x, y)) in enumerate(shape):
                if i in [33, 8, 36, 45, 48, 54]:
                    image_points[[33, 8, 36, 45, 48, 54].index(i)] = np.array([x, y], dtype='double')
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                    cv2.putText(frame, str(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                else:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                    cv2.putText(frame, str(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            for p in image_points:
                cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

            (head_tilt_degree, start_point, end_point, end_point_alt) = getHeadTiltAndCoords(size, image_points, frame_height)
            cv2.line(frame, start_point, end_point, (255, 0, 0), 2)
            cv2.line(frame, start_point, end_point_alt, (0, 0, 255), 2)

            if head_tilt_degree and int(head_tilt_degree[0]) > 20:
                cv2.putText(frame, f'Head Tilt Degree: {head_tilt_degree[0]}', (170, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                winsound.Beep(2500, 1000)
                q = detection(detected='Head Tilt Detected', time=datetime.now().time(), date=datetime.now().date(), status=1, driver_id=lid)
                q.save()
            else:
                flag += 1

        cv2.imshow("Frame", frame)
        perform_yolo_detection(frame, lid)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()

if __name__ == "__main__":
    detect("some_driver_id")