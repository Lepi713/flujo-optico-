import cv2
import numpy as np

# Global variables
selected_point = None
tracking = False
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Mouse callback function
def select_point(event, x, y, flags, param):
    global selected_point, tracking

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)
        tracking = True

# Create a named window
cv2.namedWindow('Camera Tracking')
cv2.setMouseCallback('Camera Tracking', select_point)

# Initialize the camera capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to capture video from the camera.")
        break

    if tracking and selected_point is not None:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)  # Apply Gaussian blur to the grayscale frame
        p1, _, _ = cv2.calcOpticalFlowPyrLK(gray_frame, gray_frame, np.array([selected_point], dtype=np.float32), None, **lk_params)
        selected_point = (int(p1[0][0]), int(p1[0][1]))  # Convert to integers

    if selected_point is not None:
        cv2.circle(frame, selected_point, 5, (0, 0, 255), -1)

    cv2.imshow('Camera Tracking', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
